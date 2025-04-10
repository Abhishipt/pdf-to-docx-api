from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import os
import uuid
from flask_cors import CORS
CORS(app)
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    pdf_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(pdf_path)

    # Read PDF
    doc = Document()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                doc.add_paragraph(text)
                doc.add_paragraph("\n--- Page Break ---\n")

    docx_filename = filename.rsplit('.', 1)[0] + '.docx'
    docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
    doc.save(docx_path)

    return send_file(docx_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
