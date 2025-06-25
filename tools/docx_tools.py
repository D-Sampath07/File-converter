import platform
import os
import shutil

def convert(input_path, output_path, target_format):
    ext = target_format.lower()
    
    if ext == 'pdf':
        convert_docx_to_pdf(input_path, output_path)
    elif ext == 'txt':
        docx_to_txt(input_path, output_path)
    else:
        raise ValueError(f"Unsupported target format for DOCX: {target_format}")

def convert_docx_to_pdf(input_path, output_path):
    if platform.system() == "Windows":
        from docx2pdf import convert
        temp_output_folder = os.path.dirname(output_path)
        convert(input_path, temp_output_folder)
        
        # Construct expected output filename
        output_from_lib = os.path.join(temp_output_folder, os.path.basename(input_path).replace(".docx", ".pdf"))
        if os.path.exists(output_from_lib):
            os.rename(output_from_lib, output_path)
        else:
            raise FileNotFoundError("docx2pdf did not generate output as expected.")
    else:
        import pypandoc
        try:
            pypandoc.convert_file(input_path, 'pdf', outputfile=output_path)
        except Exception as e:
            raise RuntimeError("pypandoc PDF conversion failed. Ensure LaTeX is installed.") from e

def docx_to_txt(input_path, output_path):
    import docx
    doc = docx.Document(input_path)
    full_text = '\n'.join([para.text for para in doc.paragraphs])
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(full_text)
