from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Depends, Request
from minio import Minio
import asyncpg
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, create_engine, Session, select
import os
from app.domain.upload_file import _save_file_to_server, upload_to_minio
from app.models.file_manager import GestaoArquivos, UploadedFile
from app.infra.db import get_session, init_db
import aio_pika
from app.infra.config import get_settings
import json


'''
TODO
Separar as rotas user, document, auth
'''


app = FastAPI(
    title="DigitalSE",
    version="0.1.0",
    description="Sistema de gestão documental com extração de dados por OCR",
)
allow_origin = ["*"]

settings = get_settings()

'''
class UploadedFile(BaseModel):
    user_id: int
    document_id: int
    file_name: str
'''

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origin,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# Configurações do Minio
minio_client = Minio(settings.MINIO_URL,
                      access_key=settings.MINIO_ACCESS_KEY,
                      secret_key=settings.MINIO_SECRET_KEY,
                      secure=settings.MINIO_SECURE)


# Modelo de dados
class Image(BaseModel):
    id: int
    path: str


# Conexão com o PostgreSQL
async def connect_db():
    return await asyncpg.connect(DATABASE_URL)

#FastAPIInstrumentor.instrument_app(app)

#tracer = trace.get_tracer(__name__)


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
    #logger.debug("upload images endpoint accessed")
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
        uploaded_files = UploadedFile(user_id=owner, document_id=arquivo_db.id, file_name=image_name)
        message_body = json.dumps(uploaded_files.dict())

        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
        async with connection:
            channel = await connection.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=message_body.encode()),
                routing_key="ocr",
            )
        # Fechar a conexão
        await connection.close()
        return {"message": "Upload successful"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

# Endpoint para listar as imagens
@app.get("/images/", response_model=List[GestaoArquivos])
async def list_images(session: Session = Depends(get_session)):
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
