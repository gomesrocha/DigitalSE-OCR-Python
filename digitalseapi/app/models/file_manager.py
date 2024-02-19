from sqlmodel import Field, SQLModel
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class GestaoArquivos(SQLModel, table=True):

    __tablename__ = "gestaoarquivos"
    
    id: Optional[int] = Field(primary_key=True)
    titulo: Optional[str] = Field(max_length=255)
    descricao: Optional[str] = Field(max_length=255)
    responsavel: Optional[str] = Field(max_length=255)
    data: Optional[datetime] = Field(default=datetime.now())
    localizacao: Optional[str] = Field(max_length=255)
