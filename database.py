import sqlite3
from datetime import datetime
import json
import hashlib
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


class DrawingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('drawings.db', check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            api_key_encrypted TEXT,
            api_key_salt TEXT,
            created_at DATETIME
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS drawings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            image_data TEXT,
            gemini_analysis TEXT,
            timestamp DATETIME,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        cursor.execute("PRAGMA table_info(drawings)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'user_id' not in columns:

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS drawings_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                image_data TEXT,
                gemini_analysis TEXT,
                timestamp DATETIME,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
            ''')

            cursor.execute('''
            INSERT INTO drawings_new (id, image_data, gemini_analysis, timestamp)
            SELECT id, image_data, gemini_analysis, timestamp FROM drawings
            ''')

            cursor.execute('DROP TABLE drawings')
            cursor.execute('ALTER TABLE drawings_new RENAME TO drawings')

        self.conn.commit()

    def register_user(self, username, password):
        cursor = self.conn.cursor()

        cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
        if cursor.fetchone():
            return False, "Username already exists"

        salt = os.urandom(16)
        salt_hex = salt.hex()

        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000  # Number of iterations
        ).hex()

        cursor.execute(
            'INSERT INTO users (username, password_hash, salt, created_at) VALUES (?, ?, ?, ?)',
            (username, password_hash, salt_hex, datetime.now())
        )
        self.conn.commit()

        return True, cursor.lastrowid

    def authenticate_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, password_hash, salt FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if not user:
            return False, "Invalid username or password"

        user_id, stored_hash, salt_hex = user
        salt = bytes.fromhex(salt_hex)

        # Hash the provided password with the same salt
        password_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        ).hex()

        if password_hash != stored_hash:
            return False, "Invalid username or password"

        return True, user_id

    def save_api_key(self, user_id, api_key, password):
        cursor = self.conn.cursor()

        cursor.execute('SELECT salt FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        if not result:
            return False, "User not found"

        user_salt = bytes.fromhex(result[0])

        api_key_salt = os.urandom(16)
        api_key_salt_hex = api_key_salt.hex()

        # Derive encryption key from password and user salt
        key = self._derive_key(password, user_salt)

        # Encrypt the API key
        f = Fernet(key)
        encrypted_api_key = f.encrypt(api_key.encode('utf-8')).decode('utf-8')

        # Save the encrypted API key and its salt
        cursor.execute(
            'UPDATE users SET api_key_encrypted = ?, api_key_salt = ? WHERE id = ?',
            (encrypted_api_key, api_key_salt_hex, user_id)
        )
        self.conn.commit()

        return True, "API key saved successfully"

    def get_api_key(self, user_id, password):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT salt, api_key_encrypted FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        # If user not found or no API key stored
        if not result or not result[1]:
            return None

        user_salt, encrypted_api_key = result
        user_salt = bytes.fromhex(user_salt)

        # Derive the same encryption key from password and user salt
        key = self._derive_key(password, user_salt)

        # Decrypt the API key
        try:
            f = Fernet(key)
            decrypted_api_key = f.decrypt(
                encrypted_api_key.encode('utf-8')).decode('utf-8')
            return decrypted_api_key
        except Exception as e:
            print(f"Error decrypting API key: {e}")
            return None

    def _derive_key(self, password, salt):
        """Derive a Fernet key from a password and salt."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode('utf-8')))
        return key

    def save_drawing(self, image_data, user_id=None, gemini_analysis=None):
        cursor = self.conn.cursor()
        # Remove the data:image/png;base64 prefix if present
        if ',' in image_data:
            image_data = image_data.split(',')[1]

        cursor.execute(
            'INSERT INTO drawings (user_id, image_data, gemini_analysis, timestamp) VALUES (?, ?, ?, ?)',
            (user_id, image_data, json.dumps(gemini_analysis)
             if gemini_analysis else None, datetime.now())
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_user_drawings(self, user_id):
        """Get all drawings for a specific user"""
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT * FROM drawings WHERE user_id = ? ORDER BY timestamp DESC', (user_id,))
        drawings = cursor.fetchall()

        # Parse JSON gemini_analysis back to string
        parsed_drawings = []
        for drawing in drawings:
            try:
                gemini_analysis = json.loads(
                    drawing[3]) if drawing[3] else None
            except (json.JSONDecodeError, IndexError) as e:
                print(f"Error parsing JSON for drawing {drawing[0]}: {e}")
                gemini_analysis = None

            parsed_drawings.append({
                'id': drawing[0],
                'user_id': drawing[1],
                'image_data': drawing[2],
                'analysis': gemini_analysis,
                'timestamp': drawing[4]
            })
        return parsed_drawings

    def get_drawing(self, drawing_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM drawings WHERE id = ?', (drawing_id,))
        drawing = cursor.fetchone()

        if drawing:
            return {
                'id': drawing[0],
                'user_id': drawing[1],
                'image_data': drawing[2],
                'analysis': json.loads(drawing[3]) if drawing[3] else None,
                'timestamp': drawing[4]
            }
        return None

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT id, username, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()

        if user:
            return {
                'id': user[0],
                'username': user[1],
                'created_at': user[2],
                'has_api_key': self._user_has_api_key(user[0])
            }
        return None

    def _user_has_api_key(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            'SELECT api_key_encrypted FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        return result and result[0] is not None

    def remove_api_key(self, user_id, password):
        """Remove the API key for a user after password verification"""
        cursor = self.conn.cursor()

        # First verify the password
        cursor.execute('SELECT username FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()
        if not result:
            return False, "User not found"

        username = result[0]
        success, _ = self.authenticate_user(username, password)
        if not success:
            return False, "Invalid password"

        # Remove the API key and salt
        cursor.execute(
            'UPDATE users SET api_key_encrypted = NULL, api_key_salt = NULL WHERE id = ?',
            (user_id,)
        )
        self.conn.commit()

        return True, "API key removed successfully"

    def close(self):
        self.conn.close()