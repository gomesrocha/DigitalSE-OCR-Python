from faststream import FastStream
from faststream.rabbit import RabbitBroker
from minio import Minio
from io import BytesIO
from PIL import Image
import pytesseract
import json
from pydantic import BaseModel
import re
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient


broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672")
app = FastStream(broker)

minio_bucket = "images"

minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)

# Configuração do MongoDB
mongo_client = AsyncIOMotorClient("mongodb://mongo:27017/")
db = mongo_client["document_db"]
collection = db["documents"]


class UploadedFile(BaseModel):
    user_id: int
    document_id: int
    file_name: str


def clean_and_tokenize(text):
    # Remover espaços e símbolos indesejados usando expressão regular
    cleaned_text = re.sub(r'[^\w\s]', '', text)
    # Dividir o texto em tokens usando espaços como delimitador
    tokens = cleaned_text.split()
    return tokens


async def index_document(document_id, tokens):
    for token in tokens:
        await collection.update_one(
            {"_id": token},
            {"$addToSet": {"documents": document_id}},
            upsert=True
        )

async def search_documents(keyword):
    result = await collection.find_one({"_id": keyword})
    if result:
        return result.get("documents", [])
    else:
        return []



@broker.subscriber("ocr")
async def handle(message):
    print(message)
    try:
        uploaded_file = UploadedFile(**message)
        print("User ID:", uploaded_file.user_id)
        print("Document ID:", uploaded_file.document_id)
        print("File Name:", uploaded_file.file_name)
    
        objeto = minio_client.get_object(minio_bucket, uploaded_file.file_name)
        imagem_bytes = objeto.read()
        imagem = Image.open(BytesIO(imagem_bytes))

            # Extrair texto usando Tesseract
        texto_extraido = pytesseract.image_to_string(imagem)
        tokens = clean_and_tokenize(texto_extraido)

            # Imprimir o texto extraído
        print(tokens)
        await index_document(uploaded_file.document_id, tokens)
    except Exception as e:
        print(f"Erro ao transformar a mensagem em uma instância Pydantic: {e}")
