# Air Draw

A web application that allows users to draw in the air using hand gestures, captured by their webcam. This app uses computer vision for hand tracking, real-time drawing capabilities, and AI-powered analysis of drawings.

You can see a live demo [Here](https://bit.ly/air-draw) but most propbaly it will be choppy as its a free server. For better experiance host it yourself.

## Features

- ✨ **Air Drawing**: Draw using only hand gestures (thumb and index finger pinch)
- 🎨 **Drawing Controls**: Customize line thickness, color, and pinch sensitivity
- 🔍 **AI Analysis**: Drawings are analyzed by Google's Gemini AI (when an API key is provided)
- 🔐 **User Accounts**: Register, login, and manage your API key securely
- 📱 **Responsive Design**: Works on desktop and mobile devices with cameras
- 📊 **Library**: View and manage your saved drawings

## How It Works

The application uses:

- MediaPipe for hand tracking and gesture recognition
- Flask and Socket.IO for real-time communication
- Google's Gemini AI for drawing analysis
- Modern security practices for user authentication and data protection

## Installation

### Prerequisites

- Python 3.8+
- Webcam
- (Optional) Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/anishgowda21/Air-Draw.git
   cd Air-Draw
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root (optional):

   ```
   SECRET_KEY=your_secure_random_key
   ```

5. Run the application:

   ```bash
   python app.py
   ```

6. Open your browser and navigate to:
   ```
   http://localhost:5001
   ```

## Usage

1. **Register or Login**: Create an account to save drawings and add your Gemini API key(which will be encrypted and stored only decrypted by your password)
2. **Drawing**:
   - Allow camera access when prompted
   - Pinch your thumb and index finger together to start drawing
   - Move your hand while maintaining the pinch to draw
   - Release the pinch to stop drawing
3. **Controls**:
   - Adjust line thickness and color using the controls panel
   - Use the 'Min Pinch Distance' slider to adjust sensitivity
   - Click 'Save Drawing' to save your creation
4. **View Drawings**:
   - Navigate to the drawings page to see your saved drawings
   - Click on any drawing to view details and AI analysis (if available)

## Important Notes

- **This is a demonstration application** and uses SQLite for data storage
- **SQLite database may be reset**: If you cannot login, simply register again with the same username


## Technologies Used

- **Backend**: Flask, Socket.IO, SQLite, MediaPipe
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **AI**: Google Gemini API for image analysis
- **Security**: Cryptography, PBKDF2, Fernet encryption


## Libraries

- [MediaPipe](https://mediapipe.dev/) by Google for hand tracking capabilities
- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Socket.IO](https://socket.io/) for real-time communication
- [Google Gemini](https://ai.google.dev/) for AI-powered analysis

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This application is for educational and demonstration purposes only. The drawing analysis is powered by Google's Gemini API and requires users to supply their own API key for full functionality.