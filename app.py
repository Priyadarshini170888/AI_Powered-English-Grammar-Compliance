
from flask import Flask, request, jsonify, send_file, render_template
import os
from werkzeug.utils import secure_filename
from utils import extract_text_from_file, analyze_text, correct_text, save_text_to_file

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'
ALLOWED_EXTENSIONS = {'pdf', 'docx'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file_upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_file(filepath)
        report = analyze_text(text)

        return jsonify({'report': report, 'message': 'Upload successful. Use /correct to generate corrected file.'}), 200
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/correction', methods=['POST'])
def correct_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        text = extract_text_from_file(filepath)
        corrected_text = correct_text(text)

        print("Original text:", text[:300])
        print("Corrected text:", corrected_text[:300])

        result_path = save_text_to_file(corrected_text, filename, app.config['RESULT_FOLDER'])
        return send_file(result_path, as_attachment=True)
    return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    app.run(host= "0.0.0.0",
            port =5001,
            debug=True)