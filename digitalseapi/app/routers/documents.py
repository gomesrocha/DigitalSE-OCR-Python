from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Optional
from sqlmodel import Session, select

from app.domain.queue import send_data_queue
from app.domain.upload_file import bucket_upload
from app.models.file_manager import GestaoArquivos, UploadedFile
from app.infra.db import get_session
from app.infra.config import get_minio_client
import json

router = APIRouter()


@router.post("/upload/")
async def upload_image(*, input_images: List[UploadFile] = File(...),
                       title: Optional[str],
                       description: Optional[str],
                       owner: Optional[str],
                       session: Session = Depends(get_session)):
    #logger.debug("upload images endpoint accessed")
    minio_client = get_minio_client()

    try:

        image_name = await bucket_upload(input_images, minio_client)

        arquivo_db = GestaoArquivos(titulo=title, descricao=description, 
                                    responsavel=owner, localizacao=image_name)
        session.add(arquivo_db)
        session.commit()
        session.refresh(arquivo_db)
        print(arquivo_db)
        uploaded_files = UploadedFile(user_id=owner, document_id=arquivo_db.id, file_name=image_name)
        message_body = json.dumps(uploaded_files.dict())

        await send_data_queue(message_body)
        return {"message": "Upload successful"}
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"Error: {err}")


# Endpoint para listar as imagens
@router.get("/images/", response_model=List[GestaoArquivos])
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
