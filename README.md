# AcuarioApp

AcuarioApp is a production-ready starter template for an aquarium management Android app built with Python, Kivy, and KivyMD.

Features:
- Aquarium tank dashboard
- Simple tank data overview
- Photo log support
- Image analysis using Pillow
- Android permission handling for camera and storage
- Build automation with GitHub Actions and Buildozer

## Project structure
```text
Acuarioapp/
├── .gitignore
├── README.md
├── requirements.txt
├── main.py
├── buildozer.spec
├── .github/
│   └── workflows/
│       └── build.yml
```

## Local development
Install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Android build
Install Buildozer:
```bash
pip install buildozer
```

Then build:
```bash
buildozer android debug
```

## Notes
- The app is designed to support aquarium photo logs and visual inspection workflows.
- You can extend it with:
  - water quality tracking
  - feeding logs
  - maintenance reminders
  - fish species database
  - automatic image analysis
  - camera capture integration
