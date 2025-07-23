import boto3
import os
from typing import Optional, Dict, Any
from config.logger import log


class S3Client:
    """Modern S3 client with proper error handling and logging."""
    
    def __init__(self, bucket_name: str, region: str = "us-east-1"):
        self.bucket_name = bucket_name
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=region
        )
        log.info(f"S3 client initialized for bucket: {bucket_name}")
    
    def upload(self, local_path: str, s3_key: str) -> bool:
        """Upload a file to S3 with error handling."""
        try:
            self.client.upload_file(local_path, self.bucket_name, s3_key)
            log.info(f"Uploaded {local_path} to s3://{self.bucket_name}/{s3_key}")
            return True
        except Exception as e:
            log.error(f"Upload failed for {local_path}: {e}")
            return False
    
    def download(self, s3_key: str, local_path: str) -> bool:
        """Download a file from S3 with error handling."""
        try:
            self.client.download_file(self.bucket_name, s3_key, local_path)
            log.info(f"Downloaded s3://{self.bucket_name}/{s3_key} to {local_path}")
            return True
        except Exception as e:
            log.error(f"Download failed for {s3_key}: {e}")
            return False
    
    def list_objects(self, prefix: str = "") -> Optional[list]:
        """List objects in S3 bucket with optional prefix."""
        try:
            response = self.client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix
            )
            objects = response.get('Contents', [])
            log.info(f"Listed {len(objects)} objects with prefix: {prefix}")
            return objects
        except Exception as e:
            log.error(f"List objects failed: {e}")
            return None
    
    def delete_object(self, s3_key: str) -> bool:
        """Delete an object from S3."""
        try:
            self.client.delete_object(Bucket=self.bucket_name, Key=s3_key)
            log.info(f"Deleted s3://{self.bucket_name}/{s3_key}")
            return True
        except Exception as e:
            log.error(f"Delete failed for {s3_key}: {e}")
            return False
    
    def object_exists(self, s3_key: str) -> bool:
        """Check if an object exists in S3."""
        try:
            self.client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return True
        except Exception:
            return False
    
    def get_object_metadata(self, s3_key: str) -> Optional[Dict[str, Any]]:
        """Get metadata for an S3 object."""
        try:
            response = self.client.head_object(Bucket=self.bucket_name, Key=s3_key)
            return response
        except Exception as e:
            log.error(f"Failed to get metadata for {s3_key}: {e}")
            return None


# Backward compatibility
class Bucket(S3Client):
    """Legacy Bucket class for backward compatibility."""
    
    def __init__(self, id: str, key: str, region: str):
        super().__init__(bucket_name=id, region=region)
    
    def upload(self, path: str, bucket: str, name: str):
        """Legacy upload method."""
        return super().upload(path, name)
    
    def download(self, bucket: str, path: str, name: str):
        """Legacy download method."""
        return super().download(path, name)

