from sqlmodel import Field, SQLModel, Relationship
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel


class Token(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str


class GestaoArquivos(SQLModel, table=True):

    __tablename__ = "gestaoarquivos"
    
    id: Optional[int] = Field(primary_key=True)
    titulo: Optional[str] = Field(max_length=255)
    descricao: Optional[str] = Field(max_length=255)
    responsavel: Optional[str] = Field(max_length=255)
    data: Optional[datetime] = Field(default=datetime.now())
    localizacao: Optional[str] = Field(max_length=255)
    tokens: List["Token"] = Relationship(back_populates="GestaoArquivos")


# Definir modelo para a tabela de associação entre documentos e tokens
class DocumentToken(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    document_id: int = Field(foreign_key="GestaoArquivos.id")
    token_id: int = Field(foreign_key="token.id")

    # Relacionamentos
    document: Optional["GestaoArquivos"] = Relationship(back_populates="tokens_association")
    token: Optional["Token"] = Relationship(back_populates="documents_association")


# Adicionar relação muitos para muitos entre Document e Token
GestaoArquivos.tokens_association = Relationship(
    to=Token,
    secondary=DocumentToken.__tablename__,
    back_populates="GestaoArquivos"
)

# Adicionar relação muitos para muitos entre Token e Document
Token.documents_association = Relationship(
    to=GestaoArquivos,
    secondary=DocumentToken.__tablename__,
    back_populates="tokens"
)