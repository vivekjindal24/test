import hashlib
from pathlib import Path
import boto3
from fastapi import UploadFile
from app.core.config import get_settings

settings = get_settings()

class StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            region_name=settings.s3_region,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
        )

    async def save(self, file: UploadFile, project_id: int, user_id: int) -> str:
        content = await file.read()
        checksum = hashlib.sha256(content).hexdigest()
        key = f"projects/{project_id}/users/{user_id}/{checksum}-{file.filename}"
        self.s3.put_object(Bucket=settings.s3_bucket, Key=key, Body=content, ContentType=file.content_type)
        return key

    def generate_presigned(self, key: str, expires_in: int = 3600) -> str:
        return self.s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket, "Key": key},
            ExpiresIn=expires_in,
        )
