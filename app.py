import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import threading
import time

# Import all converters
from converters.pdf_to_docx import pdf_to_docx
from converters.pdf_to_txt import pdf_to_txt
from converters.docx_to_txt import docx_to_txt
from converters.txt_to_docx import txt_to_docx
from converters.txt_to_pdf import txt_to_pdf
from converters.pptx_to_pdf import pptx_to_pdf
from converters.image_to_pdf import image_to_pdf

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
CONVERTED_FOLDER = "converted"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(CONVERTED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/convert', methods=['POST'])
def convert():
    print("✅ request.files keys:", request.files.keys())
    print("✅ request.form keys:", request.form.keys())
    print("📂 Uploaded files:", request.files)
    print("📨 input_type:", request.form.get("input_type"))
    print("📨 output_type:", request.form.get("output_type"))

    input_type = request.form.get('input_type')
    output_type = request.form.get('output_type')
    print("✅ request.files keys:", request.files.keys())
    print("🔍 Received input_type:", input_type)
    print("🔍 Received output_type:", output_type)
    print("📂 Uploaded files:", request.files)

    try:
        if input_type == "image" and output_type == "pdf":
            uploaded_files = request.files.getlist("file")
            if not uploaded_files:
                return "No image files uploaded", 400

            image_paths = []
            for f in uploaded_files:
                if f.filename == '':
                    continue
                fname = secure_filename(f.filename)
                path = os.path.join(UPLOAD_FOLDER, fname)
                f.save(path)
                image_paths.append(path)

            if not image_paths:
                return "No valid images to convert", 400

            if len(image_paths) == 1:
                first_image_name = os.path.splitext(os.path.basename(image_paths[0]))[0]
                output_file = os.path.join(CONVERTED_FOLDER, f"{first_image_name}_converted.{output_type}")
                download_name = f"{first_image_name}_converted.{output_type}"
            else:
                output_file = os.path.join(CONVERTED_FOLDER, f"images_merged_converted.{output_type}")
                download_name = f"images_merged_converted.{output_type}"
            image_to_pdf(image_paths, output_file)
            if len(image_paths) == 1:
                first_image_name = os.path.splitext(os.path.basename(image_paths[0]))[0]
                download_name = f"{first_image_name}_converted.{output_type}"
            else:
                download_name = f"images_merged_converted.{output_type}"
            print(f"📥 Sending file: {output_file} as {download_name}")
            return send_file(
                output_file, 
                as_attachment=True,
                download_name=download_name
            )
        if 'file' not in request.files or request.files['file'].filename == '':
            return "No file uploaded", 400

        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        uploaded_file.save(file_path)

        base_name = os.path.splitext(filename)[0]
        output_file = os.path.join(CONVERTED_FOLDER, f"{base_name}_converted.{output_type}")

        if input_type == "pdf" and output_type == "docx":
            pdf_to_docx(file_path, output_file)
        elif input_type == "pdf" and output_type == "txt":
            pdf_to_txt(file_path, output_file)
        elif input_type == "docx" and output_type == "txt":
            docx_to_txt(file_path, output_file)
        elif input_type == "txt" and output_type == "docx":
            txt_to_docx(file_path, output_file)
        elif input_type == "txt" and output_type == "pdf":
            txt_to_pdf(file_path, output_file)
        elif input_type == "pptx" and output_type == "pdf":
            pptx_to_pdf(file_path, output_file)
        else:
            return f"Unsupported conversion: {input_type} to {output_type}", 400

        return send_file(output_file, as_attachment=True, download_name=os.path.basename(output_file))

    except Exception as e:
        return f"Conversion failed: {e}", 500

    finally:
        def delayed_cleanup(files):
            time.sleep(1)  # wait a bit for the file to finish sending
            for f in files:
                if os.path.exists(f):
                    try:
                        os.remove(f)
                    except Exception as e:
                        print(f"⚠️ Could not delete {f}: {e}")

        if input_type == "image" and output_type == "pdf":
            cleanup_files = image_paths + [output_file]
        else:
            cleanup_files = [file_path, output_file]

        threading.Thread(target=delayed_cleanup, args=(cleanup_files,)).start()

# ✅ Add this to run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
