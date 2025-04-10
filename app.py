from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from pdf2docx import Converter
import os
import uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/convert', methods=['POST'])
def convert_pdf_to_docx():
    if 'pdfFile' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['pdfFile']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        unique_filename = f"{uuid.uuid4()}.pdf"
        pdf_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        docx_path = os.path.join(UPLOAD_FOLDER, unique_filename.replace('.pdf', '.docx'))

        file.save(pdf_path)

        try:
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()

            return send_file(docx_path, as_attachment=True, download_name='converted.docx')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

        finally:
            # Optional: clean up files if needed
            pass

    return jsonify({'error': 'Unknown error'}), 500

@app.route('/')
def index():
    return 'PDF to DOCX API is running.'

if __name__ == '__main__':
    app.run(debug=True)
