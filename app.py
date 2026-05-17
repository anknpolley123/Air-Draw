from flask import Flask, abort, render_template, request, redirect, url_for, session, flash
from flask_socketio import SocketIO
import cv2
import os
import numpy as np
import base64
from engineio.payload import Payload
from database import DrawingDatabase
from gemini_helper import GeminiHelper
from hand_tracker import HandTracker
from dotenv import load_dotenv
from auth import login_required, optional_login, get_current_user, get_api_key
from datetime import timedelta

load_dotenv()


Payload.max_decode_packets = 500

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
socketio = SocketIO(app, cors_allowed_origins="*", ping_timeout=600)

# Initialize hand tracker
hand_tracker = HandTracker()


@app.after_request
def add_security_headers(response):

    # Content Security Policy
    csp = (
        "default-src 'self'; "
        "script-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline'; "
        "style-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com 'unsafe-inline'; "
        "img-src 'self' data:; "
        "font-src 'self' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
        "connect-src 'self'"
    )
    response.headers['Content-Security-Policy'] = csp

    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'

    return response


def process_base64_image(base64_string, flip_horizontal=True):
    """Process and optionally flip a base64 encoded image."""
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]

    # Decode base64 to bytes
    image_bytes = base64.b64decode(base64_string)
    nparr = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Flip the image horizontally if needed
    if flip_horizontal and image is not None:
        image = cv2.flip(image, 1)

    return image


def encode_image_to_base64(image):
    """Convert an OpenCV image to base64 string."""
    _, buffer = cv2.imencode('.png', image)
    return base64.b64encode(buffer).decode('utf-8')


@app.route('/')
@optional_login
def index(user=None):
    return render_template('index.html', user=user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('login.html')

        db = DrawingDatabase()
        try:
            success, result = db.authenticate_user(username, password)
            if success:
                session['user_id'] = result
                session['username'] = username

                api_key = db.get_api_key(result, password)
                if api_key:
                    session['api_key'] = api_key

                flash('Login successful!', 'success')
                next_page = request.args.get('next')
                if next_page:
                    return redirect(next_page)
                return redirect(url_for('index'))
            else:
                flash(result, 'danger')
        finally:
            db.close()

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        gemini_api_key = request.form.get('gemini_api_key')

        if not username or not password:
            flash('Username and password are required', 'danger')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')

        db = DrawingDatabase()
        try:
            success, result = db.register_user(username, password)
            if success:
                user_id = result

                # Save API key if provided
                if gemini_api_key:
                    db.save_api_key(user_id, gemini_api_key, password)

                # Log in the user
                session['user_id'] = user_id
                session['username'] = username
                session['api_key'] = gemini_api_key

                flash('Registration successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash(result, 'danger')
        finally:
            db.close()

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    user = get_current_user()
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('logout'))

    db = DrawingDatabase()
    try:
        # Count user's drawings - use get_user_drawings instead
        drawings = db.get_user_drawings(user['id'])
        drawing_count = len(drawings)

        return render_template('profile.html', user=user, drawing_count=drawing_count)
    finally:
        db.close()


@app.route('/update_api_key', methods=['POST'])
@login_required
def update_api_key():
    user = get_current_user()
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('logout'))

    gemini_api_key = request.form.get('gemini_api_key')
    password = request.form.get('password')

    if not gemini_api_key or not password:
        flash('API key and password are required', 'danger')
        return redirect(url_for('profile'))

    db = DrawingDatabase()
    try:
        # Verify password
        success, _ = db.authenticate_user(user['username'], password)
        if not success:
            flash('Invalid password', 'danger')
            return redirect(url_for('profile'))

        # Save API key
        db.save_api_key(user['id'], gemini_api_key, password)

        session['api_key'] = gemini_api_key

        flash('API key updated successfully', 'success')
        return redirect(url_for('profile'))
    finally:
        db.close()


@app.route('/remove_api_key', methods=['POST'])
@login_required
def remove_api_key():
    user = get_current_user()
    if not user:
        flash('User not found', 'danger')
        return redirect(url_for('logout'))

    password = request.form.get('password')

    if not password:
        flash('Password is required to remove your API key', 'danger')
        return redirect(url_for('profile'))

    db = DrawingDatabase()
    try:
        # Remove API key
        success, message = db.remove_api_key(user['id'], password)
        session.pop('api_key', None)

        if success:
            flash('API key removed successfully', 'success')
        else:
            flash(message, 'danger')

        return redirect(url_for('profile'))
    finally:
        db.close()


@app.route('/drawings/<int:drawing_id>')
@login_required
def drawing_detail(drawing_id):
    user = get_current_user()
    db = DrawingDatabase()
    try:
        drawing = db.get_drawing(drawing_id)
        if drawing is None:
            abort(404)

        # Make sure users can only see their own drawings
        if drawing['user_id'] != user['id']:
            flash("You don't have permission to view this drawing", "danger")
            return redirect(url_for('drawings_list'))

        return render_template('drawing_detail.html', drawing=drawing, user=user)
    finally:
        db.close()


@app.route('/drawings')
@login_required
def drawings_list():
    user = get_current_user()
    db = DrawingDatabase()
    try:
        # Show only the user's drawings
        drawings = db.get_user_drawings(user['id'])
        return render_template('drawings.html', drawings=drawings, user=user)
    finally:
        db.close()


@socketio.on('process_frame')
def handle_frame(data):
    try:
        # Get frame data - don't flip for live preview
        frame = process_base64_image(data['frame'], flip_horizontal=False)
        if frame is None:
            raise ValueError("Invalid frame data")

        # Process with hand tracker
        hand_data = hand_tracker.process_and_encode_frame(frame)

        # Send processed data back to client
        socketio.emit('frame_processed', {
            'hand_data': hand_data
        }, room=request.sid)

    except Exception as e:
        print(f"Error processing frame: {e}")
        socketio.emit('frame_processed', {
            'error': str(e)
        }, room=request.sid)


@socketio.on('save_drawing')
def handle_save_drawing(data):
    try:
        # Check if user is logged in
        user_id = session.get('user_id')
        if not user_id:

            socketio.emit('drawing_saved', {
                'status': 'not_logged_in',
                'message': 'Please login or register to save your drawing'
            }, room=request.sid)
            return

        if not data or 'image' not in data:
            raise ValueError("No image data received")

        image_data = data.get('image')
        if not image_data:
            raise ValueError("Empty image data received")

        # Process the image and flip it horizontally
        image = process_base64_image(image_data, flip_horizontal=True)
        if image is None:
            raise ValueError("Failed to process image")

        # Convert back to base64
        image_data = encode_image_to_base64(image)

        # Initialize database
        db = DrawingDatabase()

        try:
            # Get user's API key if they have one
            api_key = None
            if 'api_key' in session:
                api_key = get_api_key()

            # Get analysis if user has their own API key
            analysis = None
            if api_key:
                try:
                    gemini = GeminiHelper(api_key)
                    analysis = gemini.analyze_image(image_data)
                except Exception as e:
                    print(f"Gemini analysis failed: {str(e)}")

            # Save to database with user ID
            drawing_id = db.save_drawing(image_data, user_id, analysis)

            # Return success response
            socketio.emit('drawing_saved', {
                'status': 'success',
                'drawing_id': drawing_id,
                'image_data': image_data,
                'analysis': analysis
            }, room=request.sid)

        finally:
            db.close()

    except ValueError as ve:
        print(f"Validation error: {str(ve)}")
        socketio.emit('drawing_saved', {
            'status': 'error',
            'message': str(ve)
        }, room=request.sid)
    except Exception as e:
        print(f"Error handling drawing data: {str(e)}")
        socketio.emit('drawing_saved', {
            'status': 'error',
            'message': 'Failed to process drawing'
        }, room=request.sid)


@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page handler"""
    return render_template('404.html'), 404


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5001, debug=True)