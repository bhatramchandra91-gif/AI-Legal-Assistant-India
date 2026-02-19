import pytesseract
import fitz
import easyocr

def extract_text(file_path):
    reader = easyocr.Reader(['en','hi','mr'])
    result = reader.readtext(file_path, detail=0)
    return " ".join(result)

def pdf_to_text(pdf_path):
    text=""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def ocr_ui():
    import streamlit as st
    from ocr_engine.ocr_reader import extract_text

    st.header("OCR Converter")
    file = st.file_uploader("Upload PDF/Image")

    if file:
        with open("temp.png","wb") as f:
            f.write(file.read())

        text = extract_text("temp.png")
        st.text_area("Extracted Text",text,height=300)
