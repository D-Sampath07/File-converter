from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def txt_to_pdf(txt_path, output_path):
    if not txt_path.lower().endswith(".txt"):
        raise ValueError("Input file must be a TXT file.")

    try:
        c = canvas.Canvas(output_path, pagesize=A4)
        width, height = A4
        y = height - 40  # Starting Y position

        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                if y < 40:
                    c.showPage()  # New page
                    y = height - 40
                c.drawString(40, y, line.strip())
                y -= 15  # Line spacing

        c.save()

    except Exception as e:
        raise RuntimeError(f"Failed to convert TXT to PDF: {e}")

    return output_path
