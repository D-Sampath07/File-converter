from PyPDF2 import PdfMerger, PdfReader, PdfWriter

def merge_pdfs(pdf_list, output_path):
    merger = PdfMerger()
    for pdf in pdf_list:
        merger.append(pdf)
    merger.write(output_path)
    merger.close()

def split_pdf(input_pdf, output_folder):
    reader = PdfReader(input_pdf)
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        output_file = f"{output_folder}/page_{i+1}.pdf"
        with open(output_file, "wb") as f:
            writer.write(f)

def rotate_pdf(input_pdf, output_pdf, rotation=90):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    for page in reader.pages:
        page.rotate_clockwise(rotation)  # ✅ Correct method
        writer.add_page(page)
    with open(output_pdf, "wb") as f:
        writer.write(f)
