import pdfplumber

def pdf_to_txt(pdf_path, output_path):
    if not pdf_path.lower().endswith(".pdf"):
        raise ValueError("Input file must be a PDF.")

    try:
        with pdfplumber.open(pdf_path) as pdf:
            with open(output_path, "w", encoding="utf-8") as f:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        f.write(text + "\n\n--- End of Page ---\n\n")
    except Exception as e:
        raise RuntimeError(f"Failed to convert PDF to TXT: {e}")

    return output_path
