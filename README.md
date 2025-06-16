# My Reader

This project is now a cross-platform desktop application written in Python. It reads text from TXT, PDF and DOCX files aloud using the system text‑to‑speech voices provided by `pyttsx3`.

## Features

- Open TXT, PDF or DOCX files
- Choose among installed system voices
- Play and stop playback
- Adjustable reading speed
- Highlight of currently spoken text
- Dark themed interface

## Development

Install dependencies and start the app:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
python main.py
```

Package a portable build with `PyInstaller`:

```bash
pyinstaller --onefile main.py
```
