from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import Optional
from sqlmodel import Session, select

from app.domain.queue import send_data_queue
from app.domain.upload_file import bucket_upload
from app.models.file_manager import FileManager, UploadedFile
from app.infra.db import get_session, get_mongodb_client
from app.infra.config import get_minio_client
import json
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from typing import List

class KeywordList(BaseModel):
    keywords: List[str]


router = APIRouter()


@router.post("/search")
async def search_documents(keywords: KeywordList,
                           mongodb_client: AsyncIOMotorClient = Depends(get_mongodb_client)):
    try:

        collection = mongodb_client["document_db"]["documents"]
        cursor = collection.find({"_id": {"$in": keywords.keywords}})
        documents = await cursor.to_list(length=None)

        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching documents: {e}")

@router.post("/")
async def upload_image(*, input_images: List[UploadFile] = File(...),
                       title: Optional[str],
                       description: Optional[str],
                       owner: Optional[str],
                       session: Session = Depends(get_session)):

    minio_client = get_minio_client()

    try:

        image_name = await bucket_upload(input_images, minio_client)

        arquivo_db = FileManager(title=title, description=description,
                                 owner=owner, location=image_name)
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
@router.get("/", response_model=List[FileManager])
async def list_images(session: Session = Depends(get_session)):
    try:
        # Consulta o PostgreSQL para obter os caminhos das imagens
        result = session.execute(select(FileManager))
        files = result.scalars().all()
               
        return [FileManager(id=file.id,
                            title=file.title,
                            description=file.description,
                            owner=file.owner,
                            location=file.location) for file in files]
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"PostgreSQL error: {err}")
