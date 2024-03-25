from minio import Minio
from infra.config import settings
minio_bucket = settings.MINIO_BUCKET

minio_client = Minio(settings.MINIO_URL,
                      access_key=settings.MINIO_ACCESS_KEY,
                      secret_key=settings.MINIO_SECRET_KEY,
                      secure=False)