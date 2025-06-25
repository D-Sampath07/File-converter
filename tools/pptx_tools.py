# ✅ pptx_tools.py (works on Render)
from pptx import Presentation

def pptx_to_txt(input_path, output_path):
    prs = Presentation(input_path)
    text_runs = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text_runs.append(shape.text)
    full_text = "\n".join(text_runs)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

def convert(input_path, output_path, target_format):
    if target_format == "txt":
        pptx_to_txt(input_path, output_path)
    else:
        raise ValueError(f"Conversion from PPTX to {target_format.upper()} is not supported.")
