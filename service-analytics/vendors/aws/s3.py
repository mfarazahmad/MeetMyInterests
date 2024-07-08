import boto3


# TODO: Mutex Locks

class Bucket():

    def __init__(self, id, key, region):
        self.instance = boto3.client(
            's3',
            aws_access_key_id=id,
            aws_secret_access_key=key,
            region_name=region
        )
        self.bucket = None

    def upload(self, path, bucket, name):
        self.instance.upload_file(f'{path}', bucket, f'{name}')

    def download(self, bucket, path, name):
        self.instance.download_file(bucket, path, name)

