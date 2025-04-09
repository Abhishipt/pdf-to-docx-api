from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename
import os
from docx import Document
import fitz  # PyMuPDF
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow frontend JS to access this API

@app.route('/')
def home():
    return "PDF to DOCX API is running!"

@app.route('/convert', methods=['POST'])
def convert_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save uploaded file to temp location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_pdf:
            file.save(tmp_pdf.name)

            # Convert PDF to DOCX using fitz (basic placeholder)
            output_path = tmp_pdf.name.replace('.pdf', '.docx')
            doc = Document()
            pdf_file = fitz.open(tmp_pdf.name)
            for page in pdf_file:
                text = page.get_text()
                doc.add_paragraph(text)
            doc.save(output_path)

        return send_file(output_path, as_attachment=True, download_name="converted.docx")

    except Exception as e:
        return jsonify({"error": str(e)}), 500
