from pydantic import BaseModel


class UploadedFile(BaseModel):
    user_id: int
    document_id: int
    file_name: str
