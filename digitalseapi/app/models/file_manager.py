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
class GestaoArquivos(SQLModel, table=True):
    __tablename__ = "gestaoarquivos"
    
    id: Optional[int] = Field(primary_key=True)
    titulo: Optional[str] = Field(max_length=255)
    descricao: Optional[str] = Field(max_length=255)
    responsavel: Optional[str] = Field(max_length=255)
    data: Optional[datetime] = Field(default=datetime.now())
    localizacao: Optional[str] = Field(max_length=255)

