from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from PIL import Image
import os

def image_to_pdf(image_paths, output_path):
    if isinstance(image_paths, str):
        image_paths = [image_paths]

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    for image_path in image_paths:
        if not os.path.isfile(image_path):
            raise FileNotFoundError(f"File not found: {image_path}")

        img = Image.open(image_path)
        img_width, img_height = img.size

        # Calculate scaling to fit inside A4 while preserving aspect ratio
        scale = min(width / img_width, height / img_height)
        new_width = img_width * scale
        new_height = img_height * scale

        x = (width - new_width) / 2
        y = (height - new_height) / 2

        c.drawImage(image_path, x, y, new_width, new_height)
        c.showPage()

    c.save()
    return output_path
