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


#class DocumentToken(SQLModel, table=True):
#    id: Optional[int] = Field(default=None, primary_key=True)
#    document_id: int = Field(foreign_key="gestaoarquivos.id")
#    token_id: int = Field(foreign_key="token.id")

    # Relacionamentos
#    gestaoarquivos: GestaoArquivos = Relationship(back_populates="document_tokens")
#    token: Token = Relationship()


# Adicionar relação muitos para muitos entre Document e Token
#GestaoArquivos.document_tokens = Relationship(
#    DocumentToken, back_populates="gestaoarquivos"
#)

# Adicionar relação muitos para muitos entre Token e Document
#Token.documents_association = Relationship(
#    DocumentToken, back_populates="token"
#)
