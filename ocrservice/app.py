from io import BytesIO
from PIL import Image
import pytesseract
from faststream import FastStream
from faststream.rabbit import RabbitBroker

from infra.config import settings
from infra.db import index_document
from domain.data_processing import clean_and_tokenize
from infra.bucket import minio_bucket, minio_client
from models.file import UploadedFile

broker = RabbitBroker(settings.RABBITMQ_URL)


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


app = FastStream(broker)
