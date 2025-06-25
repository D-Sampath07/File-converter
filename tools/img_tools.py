import img2pdf
import os

def convert(input_path, output_path, target_format):
    ext = input_path.rsplit('.', 1)[-1].lower()
    if target_format == 'pdf':
        convert_img_to_pdf(input_path, output_path)
    else:
        raise ValueError(f"Unsupported conversion from {ext.upper()} to {target_format.upper()}")

def convert_img_to_pdf(image_path, output_path):
    try:
        with open(output_path, "wb") as f:
            f.write(img2pdf.convert(image_path))
    except Exception as e:
        raise RuntimeError(f"Image to PDF conversion failed: {str(e)}")
