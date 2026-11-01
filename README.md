# Air Draw

<p align="left">
  <a href="https://www.instagram.com/itz_vorzhevik_volnyshev?igsh=OTNqMndzdDFzZ293"><img src="https://img.shields.io/badge/Instagram-Main-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram main" /></a>
  <a href="https://www.instagram.com/its_ankon_polley?igsh=MXQyNnVpcGV2bmF5aw=="><img src="https://img.shields.io/badge/Instagram-Alt-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram alternate" /></a>
  <a href="https://x.com/AnkonPolley"><img src="https://img.shields.io/badge/X-Follow-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" /></a>
  <a href="https://www.threads.net/@itz_vorzhevik_volnyshev"><img src="https://img.shields.io/badge/Threads-Follow-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads" /></a>
</p>
<p align="left">
  <a href="https://www.facebook.com/share/1DrXE7djH1/"><img src="https://img.shields.io/badge/Facebook-Connect-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook" /></a>
  <a href="https://www.reddit.com/u/robertoppenheimer123/s/1lsT0KNM9r"><img src="https://img.shields.io/badge/Reddit-Profile-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit" /></a>
  <a href="https://pin.it/3uKE8ZdFc"><img src="https://img.shields.io/badge/Pinterest-Saves-E60023?style=for-the-badge&logo=pinterest&logoColor=white" alt="Pinterest" /></a>
</p>

Air Draw is a webcam-based drawing web app. It tracks hand landmarks and lets you draw on a canvas by bringing your thumb and index finger together. You can adjust drawing colour, line thickness, and pinch sensitivity, and optionally request AI analysis of saved drawings with your own Google Gemini API key.

> **Project status:** Educational/demo software. Review the security and privacy notes below before running it, especially before making it available to other people.

## Features

- **Gesture drawing:** use a thumb-and-index-finger pinch to draw in the air.
- **Live hand tracking:** MediaPipe processes camera frames on the Python server.
- **Drawing controls:** adjust pinch distance, line thickness, and colour.
- **Saved drawing library:** register or sign in to save and revisit drawings.
- **Optional AI analysis:** send a saved drawing to Google Gemini when you configure your own API key.
- **Account and profile pages:** manage your account and Gemini API key.
- **Responsive web interface:** Flask templates, HTML/CSS/JavaScript, and Bootstrap.

## How it works

1. The browser asks permission to use the camera.
2. Camera frames are sent over Socket.IO to the Flask server.
3. MediaPipe identifies hand landmarks; the browser uses the returned positions to draw on the canvas.
4. When you choose to save a drawing while signed in, the image is stored in the local SQLite database.
5. If a Gemini API key is configured, the saved drawing image is sent to Google's Gemini service for analysis.

## Requirements

- Python 3.10 is recommended (the included Dockerfile uses Python 3.10).
- A webcam and a modern browser that supports camera access.
- pip and venv.
- Optional: a Google Gemini API key for AI analysis.
- On Linux, OpenCV may need system libraries for camera/image processing.

## Step-by-step: run locally

### 1. Get the source code

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

If installation fails, check that your Python version and platform are compatible with the pinned MediaPipe, OpenCV, and NumPy versions in requirements.txt.

### 4. Configure a secret key

The app currently falls back to a predictable development secret if SECRET_KEY is not set. **Do not use that default for a shared or public instance.** Set a unique random value in your local environment before starting the app.

**Linux / macOS**
~~~bash
export SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
~~~

**Windows PowerShell**
~~~powershell
$env:SECRET_KEY = (py -c "import secrets; print(secrets.token_hex(32))")
~~~

The app calls load_dotenv(), so you can also create a local .env file containing SECRET_KEY=your-long-random-value. Do not commit .env or share its contents. Use a different secret for each deployment.

### 5. Start the application

~~~bash
python app.py
~~~

Open **http://127.0.0.1:5001** in a browser on the same device. If camera access is blocked, check the browser's camera permissions. Browsers generally require HTTPS for camera access on remote hosts; localhost is treated as a secure context by modern browsers.

### 6. Try drawing

1. Open the home page and allow camera access.
2. Keep your hand visible and bring your thumb and index finger together to draw.
3. Adjust **Min Pinch Distance**, **Line Thickness**, and **Drawing Color**.
4. Select **Clear Canvas** to clear the current canvas.
5. Register or sign in, then select **Save Drawing** to store a drawing.
6. Open the drawings page to view saved work.

### 7. Optional: configure Gemini

You can provide your own Gemini API key through the app's registration/profile interface. Review Google's current terms and privacy documentation before using the service. A drawing image is sent to Google's service when AI analysis is requested. Never put an API key into source code, screenshots, issue reports, or public commits.

## Docker

A Dockerfile is included. Docker can help package dependencies, but it does **not** by itself make this application safe for public hosting. The container exposes port 5001 and runs the web app; configure secrets and deployment security separately. Camera access occurs in the user's browser and the browser sends frames to the server, so the app's camera workflow still depends on the server being reachable.

Build and run only in a private development environment after reviewing the Dockerfile and application settings:

~~~bash
docker build -t air-draw .
docker run --rm -p 5001:5001 -e SECRET_KEY="replace-with-a-long-random-secret" air-draw
~~~

This is a basic development example, not a production deployment recipe. Do not expose it publicly without a security review, HTTPS, restrictive network access, appropriate session/cookie settings, and review of Socket.IO access controls.

## Project structure

~~~text
Air-Draw/
├── app.py                 # Flask routes and Socket.IO events
├── auth.py                # Login-required helpers
├── database.py            # SQLite users and saved drawings
├── gemini_helper.py       # Optional Gemini drawing analysis
├── hand_tracker.py        # MediaPipe hand tracking
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container image definition
├── templates/             # HTML templates
├── static/                # CSS and browser-side JavaScript
├── LICENSE                # GNU GPL v3
├── README.md
└── Disclaimer.md
~~~

## Privacy and security notes

- **Camera frames are sent to the server:** this project does not perform the full hand-tracking pipeline exclusively in the browser. Run it only on a server you trust.
- **Saved drawings are stored locally:** SQLite data is written to drawings.db in the application's working directory. Protect and back up that file appropriately.
- **Optional third-party processing:** when Gemini analysis is enabled, the drawing image is sent to Google. Review the provider's current policies before submitting sensitive content.
- **Secrets:** set a strong, unique SECRET_KEY; never rely on the development fallback. Keep API keys and .env files out of Git.
- **Not production-hardened:** the current code includes permissive Socket.IO CORS configuration and should receive a security review before being exposed to a network. Authentication, session handling, request limits, deployment settings, and dependencies also need review.
- **Use test accounts and non-sensitive drawings** while evaluating the project. Do not upload private images or personal information unless you understand where they are processed and stored.
- Check [Disclaimer.md](Disclaimer.md) before using or redistributing the software.

## Troubleshooting

- **Camera not starting:** allow camera permission in the browser and close other applications using the webcam.
- **Blank or slow video/drawing:** try a Chromium-based browser, check the server terminal for errors, and use a machine with enough CPU resources.
- **Dependency install errors:** use a supported Python version and install the pinned requirements in a fresh virtual environment.
- **Gemini analysis unavailable:** verify that you supplied a valid API key and that your Google AI service access and quota are active.
- **Login or saved drawings missing:** the app uses a local SQLite file. Confirm that the process is using the expected working directory and that the database file persists.

## Contributing

Bug reports and improvements are welcome. Please open an issue with reproduction steps and remove API keys, passwords, camera images, database files, and other private data from logs or attachments.

## License

This project includes a [GNU General Public License v3.0](LICENSE). Review the license and any third-party library terms before redistributing.

## Support Me

If you find the project useful, you can follow my work or share feedback through the profiles below.

<p align="left">
  <a href="https://www.instagram.com/itz_vorzhevik_volnyshev?igsh=OTNqMndzdDFzZ293"><img src="https://img.shields.io/badge/Instagram-Main-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram main" /></a>
  <a href="https://www.instagram.com/its_ankon_polley?igsh=MXQyNnVpcGV2bmF5aw=="><img src="https://img.shields.io/badge/Instagram-Alt-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram alternate" /></a>
  <a href="https://x.com/AnkonPolley"><img src="https://img.shields.io/badge/X-Follow-000000?style=for-the-badge&logo=x&logoColor=white" alt="X" /></a>
  <a href="https://www.threads.net/@itz_vorzhevik_volnyshev"><img src="https://img.shields.io/badge/Threads-Follow-000000?style=for-the-badge&logo=threads&logoColor=white" alt="Threads" /></a>
  <a href="https://www.facebook.com/share/1DrXE7djH1/"><img src="https://img.shields.io/badge/Facebook-Connect-1877F2?style=for-the-badge&logo=facebook&logoColor=white" alt="Facebook" /></a>
  <a href="https://www.reddit.com/u/robertoppenheimer123/s/1lsT0KNM9r"><img src="https://img.shields.io/badge/Reddit-Profile-FF4500?style=for-the-badge&logo=reddit&logoColor=white" alt="Reddit" /></a>
  <a href="https://pin.it/3uKE8ZdFc"><img src="https://img.shields.io/badge/Pinterest-Saves-E60023?style=for-the-badge&logo=pinterest&logoColor=white" alt="Pinterest" /></a>
</p>

## Contact

- **Email:** [ankonpolley@proton.me](mailto:ankonpolley@proton.me)
- **Issues:** [GitHub Issues](https://github.com/anknpolley123/Air-Draw/issues)

## Developer

**Ankon Polley**  
GitHub: [@anknpolley123](https://github.com/anknpolley123)

---

<p align="center">Made with care by Ankon Polley · Air Draw</p>
