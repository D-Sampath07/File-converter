# tools/img_tools.py
from PIL import Image
import img2pdf
import os

def img_to_pdf(input_path, output_path):
    with open(output_path, "wb") as f:
        f.write(img2pdf.convert(input_path))

def img_to_png(input_path, output_path):
    with Image.open(input_path) as img:
        img.save(output_path, format="PNG")

def img_to_jpg(input_path, output_path):
    with Image.open(input_path) as img:
        rgb = img.convert("RGB")
        rgb.save(output_path, format="JPEG")

def convert(input_path, target_format, output_path):
    ext = os.path.splitext(input_path)[1].lower()
    target_format = target_format.lower()

    if target_format == "pdf":
        img_to_pdf(input_path, output_path)
    elif ext in [".jpg", ".jpeg", ".png"] and target_format in ["jpg", "jpeg"]:
        img_to_jpg(input_path, output_path)
    elif ext in [".jpg", ".jpeg", ".png"] and target_format == "png":
        img_to_png(input_path, output_path)
    else:
        raise ValueError(f"Conversion from {ext} to {target_format.upper()} is not supported.")
