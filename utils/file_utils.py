import os
from io import BytesIO
import PyPDF2
import docx
from bs4 import BeautifulSoup

def extract_text_from_file(file_path, file_bytes):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    try:
        if ext == '.pdf':
            reader = PyPDF2.PdfReader(BytesIO(file_bytes))
            for page in reader.pages:
                text += page.extract_text() or ""
        elif ext == '.docx':
            doc = docx.Document(BytesIO(file_bytes))
            text = "\n".join([para.text for para in doc.paragraphs])
        elif ext in ['.html', '.htm']:
            soup = BeautifulSoup(file_bytes, 'html.parser')
            text = soup.get_text(separator='\n', strip=True)
        elif ext == '.txt':
            text = file_bytes.decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"Error extrayendo texto del archivo {file_path}: {e}")
    return text

def save_uploaded_file(upload_dir, filename, file_bytes):
    """Guarda un archivo subido en el directorio especificado."""
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, filename)
    with open(file_path, 'wb') as f:
        f.write(file_bytes)
    return file_path

def allowed_file_extension(filename, allowed_extensions=None):
    """Valida si la extensión del archivo es permitida."""
    if allowed_extensions is None:
        allowed_extensions = {'.pdf', '.docx', '.html', '.htm', '.txt'}
    ext = os.path.splitext(filename)[1].lower()
    return ext in allowed_extensions
