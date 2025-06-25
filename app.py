from flask import Flask, request, send_file, jsonify, render_template, after_this_request
from werkzeug.utils import secure_filename
import os
import traceback

# Import your tool modules
from tools import pdf_tools, docx_tools, pptx_tools, img_tools, text_tools

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx', 'txt', 'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Helper: check file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route: Serve frontend
@app.route('/')
def index():
    return render_template('index.html')  # Make sure 'templates/index.html' exists


# Route: Handle file conversion
@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided."}), 400

        file = request.files['file']
        target_format = request.form.get('target_format')

        if file.filename == '':
            return jsonify({"error": "Empty filename."}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "File type not allowed."}), 400

        if not target_format:
            return jsonify({"error": "No target format specified."}), 400

        filename = secure_filename(file.filename)
        ext = filename.rsplit('.', 1)[1].lower()
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(input_path)

        output_filename = f"{filename.rsplit('.', 1)[0]}_converted.{target_format}"
        output_path = os.path.join(app.config['OUTPUT_FOLDER'], output_filename)

        print(f"\n[📥 RECEIVED] '{filename}' ({ext}) --> {target_format}")
        print(f"[📂 Paths] Input: {input_path}")
        print(f"[📤 Output] Will save as: {output_path}\n")

        # Dispatch to converter
        try:
            if ext == 'pdf':
                pdf_tools.convert(input_path, output_path, target_format)
            elif ext == 'docx':
                docx_tools.convert(input_path, output_path, target_format)
            elif ext == 'pptx':
                pptx_tools.convert(input_path, output_path, target_format)
            elif ext in {'jpg', 'jpeg', 'png'}:
                img_tools.convert(input_path, output_path, target_format)
            elif ext == 'txt':
                text_tools.convert(input_path, output_path, target_format)
            else:
                return jsonify({"error": f"Unsupported file type: {ext}"}), 400
        except Exception as convert_err:
            print(f"[⚠️ CONVERT ERROR] {convert_err}")
            if os.path.exists(input_path):
                os.remove(input_path)
            return jsonify({"error": "Conversion failed. Check file integrity or format."}), 500

        print(f"[✅ SUCCESS] File converted successfully.\n")

        # ✅ Schedule deletion after response is sent
        @after_this_request
        def remove_files(response):
            try:
                if os.path.exists(input_path):
                    os.remove(input_path)
                    print(f"[🧹 CLEANUP] Deleted input: {input_path}")
                if os.path.exists(output_path):
                    os.remove(output_path)
                    print(f"[🧹 CLEANUP] Deleted output: {output_path}")
            except Exception as cleanup_err:
                print(f"[⚠️ CLEANUP ERROR] {cleanup_err}")
            return response

        return send_file(output_path, as_attachment=True)

    except Exception as e:
        print("\n[❌ ERROR] Exception occurred during conversion:")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# Start the Flask app
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
