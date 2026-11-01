# Air Draw 🎨

<p align="left">
  <a href="https://www.instagram.com/itz_vorzhevik_volnyshev?igsh=OTNqMndzdDFzZ293"><img src="https://img.shields.io/badge/Instagram-Main-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Main" /></a>
  <a href="https://www.instagram.com/its_ankon_polley?igsh=MXQyNnVpcGV2bmF5aw=="><img src="https://img.shields.io/badge/Instagram-Alt-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Alternate" /></a>
  <a href="https://x.com/AnkonPolley"><img src="https://img.shields.io/badge/Twitter-Follow-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" /></a>
  <a href="https://www.threads.net/@itz_vorzhevik_volnyshev"><img src="https://img.shields.io/badge/Threads-Follow-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads Profile" /></a>
  <a href="https://www.facebook.com/share/1DrXE7djH1/"><img src="https://img.shields.io/badge/Facebook-Connect-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Profile" /></a>
  <a href="https://www.reddit.com/u/robertoppenheimer123/s/1lsT0KNM9r"><img src="https://img.shields.io/badge/Reddit-Profile-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit Profile" /></a>
  <a href="https://pin.it/3uKE8ZdFc"><img src="https://img.shields.io/badge/Pinterest-Saves-E60023?style=for-the-badge&logo=pinterest&logoColor=white" alt="Pinterest Profile" /></a>
</p>

---

**Air Draw** is a webcam-based hand-gesture drawing application created by **Ankon Polley**. It lets you draw on a digital canvas by moving your hand in front of a camera and bringing your thumb and index finger together.

> **Project note:** Air Draw is an educational and creative demo. Camera frames are sent to the server for hand tracking. Read [Disclaimer.md](Disclaimer.md) and the privacy notes before running or sharing an instance.

## 📌 Project Overview

Air Draw combines Flask, Socket.IO, and MediaPipe to turn hand movement into digital drawing input.

- **Gesture drawing:** draw by pinching your thumb and index finger together.
- **Live hand tracking:** MediaPipe detects hand landmarks from camera frames.
- **Drawing controls:** adjust drawing colour, line thickness, and pinch sensitivity.
- **Saved drawings:** create an account, sign in, and save drawings in the local SQLite database.
- **Drawing library:** revisit your saved work.
- **Optional AI analysis:** request analysis of a saved drawing using your own Google Gemini API key.
- **Web interface:** browser-based interface built with Flask templates, HTML, CSS, JavaScript, and Bootstrap.

## ⚙️ How It Works

1. Open Air Draw in a supported browser and allow camera permission.
2. The browser captures camera frames and sends them to the Flask server through Socket.IO.
3. MediaPipe processes the frames and detects hand landmarks.
4. The browser uses the returned hand positions to control drawing on the canvas.
5. When signed in, you can save a drawing to the local SQLite database.
6. If you request Gemini analysis, the selected drawing image is sent to Google's Gemini service.

## ⚠️ Read Before Use

- Camera frames are transmitted to the server. Run the application only with a server you trust.
- Saved drawings and account information are stored in a local SQLite database.
- Optional Gemini analysis sends the selected drawing image to Google for processing.
- The current project configuration is intended for development and has not been hardened for public hosting.
- Set a unique `SECRET_KEY`; do not rely on the predictable development fallback.
- Review the Socket.IO CORS configuration, authentication, session handling, and deployment security before allowing network access.
- Do not upload sensitive or private images unless you understand how they are processed and stored.

Read the complete [Disclaimer](Disclaimer.md) before use.

## 🛠️ Installation

### Requirements

- Python 3.10 recommended (the included Dockerfile uses Python 3.10).
- Webcam and a modern browser.
- pip and Python virtual environment support.
- Optional: Google Gemini API key for AI drawing analysis.

### 1. Clone the repository

~~~bash
git clone https://github.com/anknpolley123/Air-Draw.git
cd Air-Draw
~~~

### 2. Create a virtual environment

**Linux / macOS**
~~~bash
python3 -m venv .venv
source .venv/bin/activate
~~~

**Windows PowerShell**
~~~powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
~~~

### 3. Install dependencies

~~~bash
python -m pip install --upgrade pip
pip install -r requirements.txt
~~~

If installation fails, check the Python version and platform compatibility of the pinned MediaPipe, OpenCV, and NumPy dependencies.

### 4. Set the Flask secret key

The application currently has a predictable fallback secret for development. Set your own random secret before running it.

**Linux / macOS**
~~~bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
~~~

**Windows PowerShell**
~~~powershell
$env:SECRET_KEY = (py -c "import secrets; print(secrets.token_hex(32))")
~~~

You can also use a local `.env` file. Do not commit that file or share its contents.

### 5. Run Air Draw

~~~bash
python app.py
~~~

Open this address in a browser on the same device:

**http://127.0.0.1:5001**

For remote access, browsers generally require HTTPS before allowing camera access. Localhost is treated as a secure context by modern browsers.

## 🎨 How to Use

1. Open the home page and allow camera access.
2. Keep your hand visible to the camera.
3. Bring your thumb and index finger together to draw.
4. Adjust **Min Pinch Distance**, **Line Thickness**, and **Drawing Color** as needed.
5. Use **Clear Canvas** to clear the current drawing.
6. Register or sign in to use **Save Drawing**.
7. Visit the drawings page to view your saved work.

## 🤖 Optional Gemini Analysis

Air Draw can use a Google Gemini API key for optional drawing analysis.

- Configure your own key through the app's account/profile interface.
- Request analysis only when you want to send a drawing for external processing.
- Review Google's current terms and privacy documentation before using the service.
- Keep API keys private. Never commit them to GitHub or include them in screenshots, logs, or public issues.

## 🐳 Docker

A Dockerfile is included for packaging the application.

~~~bash
docker build -t air-draw .
docker run --rm -p 5001:5001 -e SECRET_KEY="replace-with-a-long-random-secret" air-draw
~~~

This is a basic development example, not a production deployment configuration. Docker does not automatically secure the application. Review the Dockerfile, secrets, network access, HTTPS, Socket.IO permissions, and session settings before using a hosted instance.

## 📂 Project Structure

~~~text
Air-Draw/
├── app.py                 # Flask routes and Socket.IO events
├── auth.py                # Authentication helpers
├── database.py            # SQLite users and saved drawings
├── gemini_helper.py       # Optional Gemini analysis
├── hand_tracker.py        # MediaPipe hand tracking
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── templates/             # HTML templates
├── static/                # CSS and browser-side JavaScript
├── LICENSE                # GNU GPL v3
├── README.md
└── Disclaimer.md
~~~

## 🔐 Privacy & Security

- Camera frames are sent from the browser to the server for hand tracking.
- Saved drawings and account records are stored in the local `drawings.db` SQLite database.
- Gemini analysis sends the selected drawing image to Google's service when requested.
- Protect database files, API keys, environment files, and account credentials.
- The current code includes permissive Socket.IO CORS settings and a predictable fallback secret key. Review and change these before any network-facing deployment.
- This project has not been independently security-audited and should not be treated as production-hardened software.

## 🧭 Troubleshooting

- **Camera not starting:** allow camera permission in your browser and close other applications using the webcam.
- **Video or drawing is slow:** try a modern Chromium-based browser and check the server terminal for errors.
- **Dependency installation fails:** use a fresh virtual environment and a compatible Python version.
- **Gemini analysis is unavailable:** verify your API key, service access, and quota.
- **Saved drawings are missing:** check the application's working directory and the local SQLite database file.

## 🤝 Contributing

Suggestions, bug reports, and improvements are welcome.

1. Fork the repository.
2. Create a branch for your changes.
3. Test your changes locally.
4. Explain the changes clearly in your pull request.

Remove passwords, API keys, private images, database files, and other sensitive information before opening an issue or pull request.

## ⚖️ License

This project includes the [GNU General Public License v3.0](LICENSE). Review the license and third-party library terms before copying, modifying, or redistributing the project.

---

## Support Me

<div align="center">

**Follow and connect with me on social media:**

<p align="center">
  <a href="https://www.instagram.com/itz_vorzhevik_volnyshev?igsh=OTNqMndzdDFzZ293"><img src="https://img.shields.io/badge/Instagram-Main-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Main" /></a>
  <a href="https://www.instagram.com/its_ankon_polley?igsh=MXQyNnVpcGV2bmF5aw=="><img src="https://img.shields.io/badge/Instagram-Alt-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram Alternate" /></a>
  <a href="https://x.com/AnkonPolley"><img src="https://img.shields.io/badge/Twitter-Follow-000000?style=for-the-badge&logo=x&logoColor=white" alt="Follow on X" /></a>
  <a href="https://www.threads.net/@itz_vorzhevik_volnyshev"><img src="https://img.shields.io/badge/Threads-Follow-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads Profile" /></a>
  <a href="https://www.facebook.com/share/1DrXE7djH1/"><img src="https://img.shields.io/badge/Facebook-Connect-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook Profile" /></a>
  <a href="https://www.reddit.com/u/robertoppenheimer123/s/1lsT0KNM9r"><img src="https://img.shields.io/badge/Reddit-Profile-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit Profile" /></a>
  <a href="https://pin.it/3uKE8ZdFc"><img src="https://img.shields.io/badge/Pinterest-Saves-E60023?style=for-the-badge&logo=pinterest&logoColor=white" alt="Pinterest Profile" /></a>
</p>

</div>

---

## 📧 Contact

<p align="left">
  <a href="mailto:ankonpolley@proton.me"><img src="https://img.shields.io/badge/Proton_Mail-Contact_Me-6D4AFF?style=for-the-badge&logo=protonmail&logoColor=white" alt="Contact Ankon via Proton Mail" /></a>
</p>

For project support or bug reports, visit [GitHub Issues](https://github.com/anknpolley123/Air-Draw/issues). Do not post private images, credentials, or API keys.

---

## 👨‍💻 Developer

**Ankon Polley**

Developer | Programmer | Technology Enthusiast

GitHub: [@anknpolley123](https://github.com/anknpolley123)

---

<p align="center">
  <b>Air Draw</b>
  <br>
  Turn Hand Gestures Into Digital Art.
  <br><br>
  Made with ❤️ by Ankon Polley
</p>
