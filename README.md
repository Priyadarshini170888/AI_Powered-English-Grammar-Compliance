# 📝 Grammar Compliance Checker (Flask + LanguageTool)

This project is a Flask web application that allows users to upload PDF or DOCX files, analyze them for grammatical issues using the **LanguageTool API**, and download corrected versions.

---

## 🚀 Features

- ✅ Upload `.pdf` or `.docx` files for analysis
- 🧠 Detects grammar, punctuation, and style issues
- 📥 Download auto-corrected version of the document
- 🌐 Simple web interface (HTML + CSS)
- 🔍 JSON-free, human-readable grammar issue report
- ✅ Tested with `unittest`

---

## Web UI Preview

- Upload a document to check for grammar
- View grammar issues in a styled card format
- Download corrected `.txt` file version

---

## 🗂️ Project Structure
📁 AI Powered English Grammar Compliance Checker/
├── app.py # Main Flask server
├── utils.py # Text extraction and grammar logic
├── test_app.py # Unit tests
├── requirements.txt # Dependencies
├── templates/
│ └── index.html # Web frontend (stylish HTML)
├── uploads/ # User uploaded files
└── results/ # Corrected file downloads

## Install dependencies
    pip install -r requirements.txt


## ▶️ Run the App
    python app.py
    Visit: http://127.0.0.1:5001

## 🧪 Run Unit Tests
    python test_app.py
