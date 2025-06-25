# tools/pdf_tools.py
import fitz  # PyMuPDF
import os
from pdf2image import convert_from_path

def pdf_to_txt(input_path, output_path):
    doc = fitz.open(input_path)
    text = ""
    for page in doc:
        text += page.get_text()
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

def pdf_to_images(input_path, output_path, fmt):
    images = convert_from_path(input_path)
    base = os.path.splitext(output_path)[0]
    for i, img in enumerate(images):
        img_path = f"{base}_page{i + 1}.{fmt}"
        img.save(img_path, fmt.upper())

def convert(input_path, output_path, target_format):
    if target_format == "txt":
        pdf_to_txt(input_path, output_path)
    elif target_format in ["jpg", "png"]:
        pdf_to_images(input_path, output_path, target_format)
    else:
        raise ValueError(f"Conversion from PDF to {target_format} is not supported.")
