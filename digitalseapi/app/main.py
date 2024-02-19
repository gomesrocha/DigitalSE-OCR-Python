from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from minio import Minio
import asyncpg
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Field, SQLModel, create_engine, Session
import os
import shutil
from datetime import datetime
from app.domain.upload_file import _save_file_to_server, upload_to_minio
from app.models.file_manager import GestaoArquivos

# Configurações do PostgreSQL
DATABASE_URL = "postgresql://postgres:postgres@postgres/digitalsedb"

engine = create_engine(DATABASE_URL)
SQLModel.metadata.create_all(engine)


class Arquivo(BaseModel):
    titulo: str = Field(max_length=255)
    descricao: str = Field(max_length=500)
    responsavel: str = Field(max_length=255)


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

# Endpoint para fazer upload de imagens
@app.post("/upload/")
async def upload_image(*, input_images: List[UploadFile] = File(...), 
                       title: Optional[str], 
                       description: Optional[str], 
                       owner: Optional[str]):
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
        with Session(engine) as session:
            session.add(arquivo_db)
            session.commit()
            session.refresh(arquivo_db)
            print(arquivo_db)
        return {"message": "Upload successful"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")

# Endpoint para listar as imagens
@app.get("/images/", response_model=List[Image])
async def list_images():
    try:
        # Consulta o PostgreSQL para obter os caminhos das imagens
        conn = await connect_db()
        rows = await conn.fetch("SELECT id, path FROM images")
        await conn.close()

        return [{"id": row['id'], "path": row['path']} for row in rows]
    except asyncpg.exceptions.PostgresError as err:
        raise HTTPException(status_code=500, detail=f"PostgreSQL error: {err}")

# Endpoint para exibir uma imagem
@app.get("/images/{image_id}/")
async def get_image(image_id: int):
    try:
        # Consulta o PostgreSQL para obter o caminho da imagem
        conn = await connect_db()
        row = await conn.fetchrow("SELECT path FROM images WHERE id = $1", image_id)
        await conn.close()

        if not row:
            raise HTTPException(status_code=404, detail="Image not found")

        image_path = row['path']

        # Obtém a imagem do Minio
        image_stream = minio_client.get_object("images", image_path)
        image_data = image_stream.read()

        return {"image": image_data}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")
