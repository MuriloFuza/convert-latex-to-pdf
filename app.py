import zipfile
import tempfile
import shutil
import os
import subprocess
from flask import Flask, request, send_file, jsonify, Response
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure a secure directory for temporary files
TEMP_DIR = tempfile.mkdtemp(prefix="tex2pdf_")

# Allowed extensions for the .tex file
ALLOWED_EXTENSIONS = {'tex'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    # Check for uploaded file
    if 'file' not in request.files:
        return jsonify({"error": "No file provided"}), 400

    zip_file = request.files['file']

    # Check if a file is selected
    if zip_file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check for ZIP file extension
    if not zip_file.filename.lower().endswith('.zip'):
        return jsonify({"error": "Invalid file type. Only ZIP files allowed"}), 400

    # Secure filename handling
    zip_filename = secure_filename(zip_file.filename)
    zip_path = os.path.join(TEMP_DIR, zip_filename)

    try:
        # Save the ZIP file
        zip_file.save(zip_path)

        # Extract ZIP contents
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            extracted_dir = os.path.join(TEMP_DIR, 'extracted')
            os.makedirs(extracted_dir, exist_ok=True)
            zip_ref.extractall(extracted_dir)

        # Find the .tex file
        tex_file = None
        for root, dirs, files in os.walk(extracted_dir):
            for file in files:
                if file.endswith('.tex'):
                    tex_file = os.path.join(root, file)
                    break
            if tex_file:
                break

        if not tex_file:
            return jsonify({"error": "No .tex file found in the ZIP"}), 400

        # PDF filename and path
        pdf_filename = os.path.basename(tex_file).rsplit('.', 1)[0] + '.pdf'
        pdf_path = os.path.join(TEMP_DIR, pdf_filename)

        # Execute pdflatex with working directory set to the extracted directory
        try:
            subprocess.run(
                ["xelatex", "-interaction=nonstopmode", "-output-directory", TEMP_DIR, tex_file],
                check=True,
                capture_output=True,
                text=True,
                cwd=extracted_dir
            )

            # Execute novamente o xelatex para resolver referências, se necessário
            if os.path.exists(os.path.join(TEMP_DIR, pdf_filename.rsplit('.', 1)[0] + '.aux')):
                subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", "-output-directory", TEMP_DIR, tex_file],
                    check=True,
                    capture_output=True,
                    text=True,
                    cwd=extracted_dir
                )

        except subprocess.CalledProcessError as e:
            print(f"pdflatex error: {e.stdout}\n{e.stderr}")
    except subprocess.CalledProcessError as e:
            print(f"pdflatex error: {e.stdout}\n{e.stderr}")

    # Verifica se o PDF foi gerado
    if not os.path.exists(pdf_path):
        return jsonify({"error": "PDF file was not generated"}), 500

    # Retorna o PDF gerado
    try:
        with open(pdf_path, 'rb') as f:
            pdf_data = f.read()
        
        response = Response(pdf_data, mimetype='application/pdf')
        response.headers['Content-Disposition'] = f'attachment; filename={pdf_filename}'
        return response
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    finally:
        # Limpeza dos arquivos temporários
        try:
            shutil.rmtree(extracted_dir)  # Remove arquivos extraídos
            os.remove(zip_path)  # Remove o arquivo ZIP
        except Exception as e:
            print(f"Erro ao limpar arquivos temporários: {e}")

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=5000)
