from fastapi import APIRouter, status, UploadFile, File, HTTPException, Form, Depends, Request
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
import aio_pika
router = APIRouter()

minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)

@router.post("/upload/")
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
        connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
        async with connection:
            channel = await connection.channel()

            await channel.default_exchange.publish(
                aio_pika.Message(body=image_name.encode()),
                routing_key="ocr",
            )
        # Fechar a conexão
        await connection.close()
        return {"message": "Upload successful"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")
