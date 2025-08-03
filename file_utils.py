import os
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
from docx import Document
import html2text

def extract_text_from_file(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        reader = PdfReader(file_path)
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return text
    elif ext == '.docx':
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    elif ext == '.html':
        with open(file_path, encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')
            return soup.get_text(separator='\n')
    elif ext == '.md':
        with open(file_path, encoding='utf-8') as f:
            html = markdown(f.read())
            return html2text.html2text(html)
    elif ext in ['.txt', '.csv']:
        with open(file_path, encoding='utf-8') as f:
            return f.read()
    else:
        return ""

def save_uploaded_file(uploaded_file, directory="uploads"):
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, uploaded_file.filename)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path
