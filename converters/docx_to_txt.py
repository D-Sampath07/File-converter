from docx import Document

def docx_to_txt(docx_path, output_path):
    if not docx_path.lower().endswith(".docx"):
        raise ValueError("Input file must be a DOCX file.")

    try:
        doc = Document(docx_path)
        with open(output_path, "w", encoding="utf-8") as f:
            for para in doc.paragraphs:
                f.write(para.text + "\n")
    except Exception as e:
        raise RuntimeError(f"Failed to convert DOCX to TXT: {e}")

    return output_path
