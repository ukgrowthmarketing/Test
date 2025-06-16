# My Reader

This project is a cross-platform desktop application built with Electron. It reads text from TXT, PDF, and DOCX files aloud using the system text-to-speech voices.

## Features

- Open TXT, PDF, or DOCX files
- Choose among installed system voices
- Play and stop playback
- Adjustable reading speed
- Dark themed interface

## Development

Install dependencies and start the app:

```bash
npm install
npm start
```

Use `electron-builder` to package a portable build:

```bash
npx electron-builder --dir
```
