from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, Request
from minio import Minio
import asyncpg
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
import os
from app.domain.upload_file import _save_file_to_server, upload_to_minio
from app.models.file_manager import GestaoArquivos
from app.infra.db import get_session, init_db
import logging


from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry import trace


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(
    title="DigitalSE",
    version="0.1.0",
    description="Sistema de gestão documental com extração de dados por OCR",
)
allow_origin = ["*"]




app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Configurações do Minio
minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)


# Modelo de dados
class Image(BaseModel):
    id: int
    path: str


# Conexão com o PostgreSQL
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

FastAPIInstrumentor.instrument_app(app)

tracer = trace.get_tracer(__name__)


@app.on_event("startup")
def on_startup():
    init_db()
    

# Endpoint para fazer upload de imagens
@app.post("/upload/")
async def upload_image(*, input_images: List[UploadFile] = File(...),
                       title: Optional[str],
                       description: Optional[str],
                       owner: Optional[str],
                       session: Session = Depends(get_session)):
    logger.debug("upload images endpoint accessed")
    try:
        # Salva a imagem no Minio
    

        bucket_name = "images"
        found = minio_client.bucket_exists(bucket_name)
        if not found:
            minio_client.make_bucket(bucket_name)
            print("Created bucket", bucket_name)
        else:
            print("Bucket", bucket_name, "already exists")
        image_name = ""
        for img in input_images:
            print("Images Uploaded: ", img.filename)
            temp_file = _save_file_to_server(img, path="./images/", 
                                             save_as=img.filename)
            image_name = img.filename
            # Upload file to MinIO
            upload_to_minio(minio_client, temp_file, 
                            bucket_name, img.filename)
            os.remove(temp_file)

        arquivo_db = GestaoArquivos(titulo=title, descricao=description, 
                                    responsavel=owner, localizacao=image_name)
        session.add(arquivo_db)
        session.commit()
        session.refresh(arquivo_db)
        print(arquivo_db)
        return {"message": "Upload successful"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

# Endpoint para listar as imagens
@app.get("/images/", response_model=List[GestaoArquivos])
async def list_images(session: Session = Depends(get_session)):
    logger.debug("images endpoint accessed")
    try:
        # Consulta o PostgreSQL para obter os caminhos das imagens
        result = session.execute(select(GestaoArquivos))
        arquivos = result.scalars().all()
        

        return [GestaoArquivos(id=arquivo.id, 
                            titulo=arquivo.titulo, 
                            descricao=arquivo.descricao,
                            responsavel=arquivo.responsavel,
                            localizacao=arquivo.localizacao) for arquivo in arquivos]
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"PostgreSQL error: {err}")
