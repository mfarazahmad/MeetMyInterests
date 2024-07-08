import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from ai.utils import tokenizer, context_encoder
from config.bootstrap import vectorIndex

folder_id = ""

def download_file_from_drive(file_id, file_name):
    service = build('drive', 'v3')
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    with open(file_name, 'wb') as f:
        f.write(fh.read())
    print(f"Downloaded {file_name}")

def list_pdfs_from_drive(folder_id):
    service = build('drive', 'v3')
    query = f"'{folder_id}' in parents and mimeType='application/pdf'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    return results.get('files', [])

def initialize_pdf_index():
    pdf_files = list_pdfs_from_drive(folder_id)
    chunks = []

    for pdf in pdf_files:
        file_id = pdf['id']
        file_name = pdf['name']
        download_file_from_drive(file_id, file_name)

        parsed_text = parse_pdf(file_name)
        chunk_size = 512
        for i in range(0, len(parsed_text), chunk_size):
            chunk = parsed_text[i:i + chunk_size]
            chunks.append(chunk)
            inputs = tokenizer(chunk, return_tensors='tf', padding=True, truncation=True)
            embedding = context_encoder(**inputs).pooler_output.numpy().squeeze()
            vectorIndex.update(f"pdf_{i}", embedding, chunk, 'pdfs')

    return chunks
