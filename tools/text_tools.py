from fpdf import FPDF
import os

def convert(input_path, output_path, target_format):
    if target_format.lower() == 'pdf':
        convert_txt_to_pdf(input_path, output_path)
    else:
        raise ValueError(f"Unsupported conversion from TXT to {target_format}")

def convert_txt_to_pdf(txt_path, pdf_path):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    with open(txt_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split long lines manually if needed
            pdf.multi_cell(0, 10, txt=line.strip())

    pdf.output(pdf_path)
