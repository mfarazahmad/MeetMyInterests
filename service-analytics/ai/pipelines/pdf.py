import io
from typing import List, Dict, Any

from ai.utils import embedding_generator
from config.bootstrap import vectorIndex, google_drive_client

folder_id = ""

def download_file_from_drive(file_id: str, file_name: str) -> bool:
    """Download a file from Google Drive using the new client."""
    try:
        if not google_drive_client:
            print("Google Drive client not initialized")
            return False
        
        success = google_drive_client.download_file(file_id, file_name)
        if success:
            print(f"Downloaded {file_name}")
        return success
        
    except Exception as e:
        print(f"Error downloading file: {e}")
        return False

def list_pdfs_from_drive(folder_id: str) -> List[Dict[str, Any]]:
    """List PDF files from Google Drive using the new client."""
    try:
        if not google_drive_client:
            print("Google Drive client not initialized")
            return []
        
        files = google_drive_client.list_files(folder_id=folder_id)
        if files:
            # Filter for PDF files
            pdf_files = [f for f in files if f.get('mimeType') == 'application/pdf']
            return pdf_files
        return []
        
    except Exception as e:
        print(f"Error listing PDF files: {e}")
        return []

def parse_pdf(file_name: str) -> str:
    """Parse PDF file and extract text."""
    # This is a placeholder - you'll need to implement actual PDF parsing
    # You can use libraries like PyPDF2, pdfplumber, or pdf2txt
    try:
        # Placeholder implementation
        with open(file_name, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error parsing PDF {file_name}: {e}")
        return ""

def initialize_pdf_index() -> List[str]:
    """Initialize PDF index with documents from Google Drive."""
    pdf_files = list_pdfs_from_drive(folder_id)
    chunks = []

    for pdf in pdf_files:
        file_id = pdf['id']
        file_name = pdf['name']
        
        if download_file_from_drive(file_id, file_name):
            parsed_text = parse_pdf(file_name)
            chunk_size = 512
            
            for i in range(0, len(parsed_text), chunk_size):
                chunk = parsed_text[i:i + chunk_size]
                chunks.append(chunk)
                
                # Use new embedding generator
                embedding = embedding_generator.generate_embedding(chunk)
                vectorIndex.update(f"pdf_{i}", embedding, chunk, 'pdfs')

    return chunks
