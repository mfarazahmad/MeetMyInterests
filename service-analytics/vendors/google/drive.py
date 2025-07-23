import os
import io
from typing import List, Dict, Any, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload
import pickle

from config.logger import log


class GoogleDriveClient:
    """Modern Google Drive client with authentication and file operations."""
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/drive']
    
    def __init__(self):
        self.service = None
        self.credentials = None
        self._authenticate()
    
    def _authenticate(self) -> bool:
        """Authenticate with Google Drive API."""
        try:
            creds = None
            # The file token.pickle stores the user's access and refresh tokens
            if os.path.exists('token.pickle'):
                with open('token.pickle', 'rb') as token:
                    creds = pickle.load(token)
            
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        'credentials.json', self.SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                with open('token.pickle', 'wb') as token:
                    pickle.dump(creds, token)
            
            self.credentials = creds
            self.service = build('drive', 'v3', credentials=creds)
            log.info("Google Drive authentication successful")
            return True
            
        except Exception as e:
            log.error(f"Google Drive authentication failed: {e}")
            return False
    
    def list_files(self, folder_id: str = None, query: str = None) -> Optional[List[Dict[str, Any]]]:
        """List files in Google Drive."""
        try:
            if folder_id:
                query = f"'{folder_id}' in parents"
            
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            log.info(f"Listed {len(files)} files from Google Drive")
            return files
            
        except Exception as e:
            log.error(f"Failed to list files: {e}")
            return None
    
    def upload_file(self, file_path: str, folder_id: str = None, filename: str = None) -> Optional[str]:
        """Upload a file to Google Drive."""
        try:
            if not filename:
                filename = os.path.basename(file_path)
            
            file_metadata = {'name': filename}
            if folder_id:
                file_metadata['parents'] = [folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file.get('id')
            log.info(f"Uploaded {file_path} to Google Drive with ID: {file_id}")
            return file_id
            
        except Exception as e:
            log.error(f"Failed to upload file {file_path}: {e}")
            return None
    
    def download_file(self, file_id: str, local_path: str) -> bool:
        """Download a file from Google Drive."""
        try:
            request = self.service.files().get_media(fileId=file_id)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                log.info(f"Download progress: {int(status.progress() * 100)}%")
            
            fh.seek(0)
            with open(local_path, 'wb') as f:
                f.write(fh.read())
            
            log.info(f"Downloaded file {file_id} to {local_path}")
            return True
            
        except Exception as e:
            log.error(f"Failed to download file {file_id}: {e}")
            return False
    
    def create_folder(self, folder_name: str, parent_folder_id: str = None) -> Optional[str]:
        """Create a folder in Google Drive."""
        try:
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            if parent_folder_id:
                folder_metadata['parents'] = [parent_folder_id]
            
            folder = self.service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            log.info(f"Created folder '{folder_name}' with ID: {folder_id}")
            return folder_id
            
        except Exception as e:
            log.error(f"Failed to create folder '{folder_name}': {e}")
            return None
    
    def delete_file(self, file_id: str) -> bool:
        """Delete a file from Google Drive."""
        try:
            self.service.files().delete(fileId=file_id).execute()
            log.info(f"Deleted file {file_id} from Google Drive")
            return True
            
        except Exception as e:
            log.error(f"Failed to delete file {file_id}: {e}")
            return False
    
    def search_files(self, query: str) -> Optional[List[Dict[str, Any]]]:
        """Search for files in Google Drive."""
        try:
            results = self.service.files().list(
                q=query,
                pageSize=100,
                fields="nextPageToken, files(id, name, mimeType, size, modifiedTime)"
            ).execute()
            
            files = results.get('files', [])
            log.info(f"Found {len(files)} files matching query: {query}")
            return files
            
        except Exception as e:
            log.error(f"Failed to search files: {e}")
            return None
    
    def get_file_info(self, file_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a file."""
        try:
            file = self.service.files().get(
                fileId=file_id,
                fields="id,name,mimeType,size,modifiedTime,createdTime,parents"
            ).execute()
            
            log.info(f"Retrieved info for file {file_id}")
            return file
            
        except Exception as e:
            log.error(f"Failed to get file info for {file_id}: {e}")
            return None


# Backward compatibility
class GoogleDrive(GoogleDriveClient):
    """Legacy GoogleDrive class for backward compatibility."""
    
    def connectToGoogle(self):
        """Legacy method for connecting to Google."""
        return self._authenticate()
    
    def loadGoogleDoc(self):
        """Legacy method for loading Google Docs."""
        log.warning("loadGoogleDoc is deprecated. Use get_file_info() instead.")
        pass
    
    def loadGoogleDrive(self):
        """Legacy method for loading Google Drive."""
        log.warning("loadGoogleDrive is deprecated. Use list_files() instead.")
        pass
    
    def traverseFileHierarchy(self):
        """Legacy method for traversing file hierarchy."""
        log.warning("traverseFileHierarchy is deprecated. Use list_files() instead.")
        pass