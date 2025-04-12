import threading

def schedule_file_deletion(file_paths, delay=600):  # 600 seconds = 10 minutes
    def delete_files():
        for path in file_paths:
            try:
                if os.path.exists(path):
                    os.remove(path)
                    print(f"🗑️ Deleted: {path}")
            except Exception as e:
                print(f"Error deleting {path}: {e}")
    threading.Timer(delay, delete_files).start()
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import os
import uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "PDF to DOCX API is running."


@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        unique_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, secure_filename(unique_filename))
        file.save(pdf_path)

        # 🚫 Optional: Reject files over 10 MB
        if os.path.getsize(pdf_path) > 10 * 1024 * 1024:
            os.remove(pdf_path)
            return jsonify({'error': 'File too large. Please upload a PDF smaller than 10 MB.'}), 400

        docx_path = pdf_path.replace('.pdf', '.docx')
        schedule_file_deletion([pdf_path, docx_path], delay=600)

        print(f"📥 Received: {file.filename}")
        print(f"📄 Size: {os.path.getsize(pdf_path)} bytes")
        print("🔄 Starting conversion...")

        # Convert PDF to DOCX
        cv = Converter(pdf_path)
        cv.convert(docx_path, start=0, end=None)
        cv.close()

        print("✅ Conversion successful.")
        return send_file(docx_path, as_attachment=True, download_name='converted.docx')

    except Exception as e:
        print(f"❌ Conversion error: {e}")
        return jsonify({'error': 'Conversion failed. Please try again with a simpler file.'}), 500
