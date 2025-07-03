from docx import Document
import pdfplumber
import os

def pdf_to_docx(pdf_path, output_path):
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Input file must be a PDF.")

    doc = Document()

    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)
                doc.add_page_break()
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to DOCX: {e}")

    doc.save(output_path)
    return output_path

