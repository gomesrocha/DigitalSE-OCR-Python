from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


#class Token(SQLModel, table=True):
#    id: Optional[int] = Field(default=None, primary_key=True)
#    word: str

#Data model for transfer
class UploadedFile(BaseModel):
    user_id: int
    document_id: int
    file_name: str



#Model database
class FileManager(SQLModel, table=True):
    __tablename__ = "gestaoarquivos"
    
    id: Optional[int] = Field(primary_key=True)
    title: Optional[str] = Field(max_length=255)
    description: Optional[str] = Field(max_length=255)
    owner: Optional[str] = Field(max_length=255)
    date: Optional[datetime] = Field(default=datetime.now())
    location: Optional[str] = Field(max_length=255)

