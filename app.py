from flask import Flask, request, send_file
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
CONVERTED_FOLDER = 'converted'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return "PDF to DOCX API is running!"

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return {"error": "No file part"}, 400

    file = request.files['file']
    if file.filename == '':
        return {"error": "No selected file"}, 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    output_filename = filename.rsplit('.', 1)[0] + '.docx'
    output_path = os.path.join(CONVERTED_FOLDER, output_filename)

    try:
        subprocess.run(['libreoffice', '--headless', '--convert-to', 'docx', '--outdir', CONVERTED_FOLDER, filepath], check=True)
        return send_file(output_path, as_attachment=True)
    except subprocess.CalledProcessError:
        return {"error": "Conversion failed"}, 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)

if __name__ == '__main__':
    app.run(debug=True)
