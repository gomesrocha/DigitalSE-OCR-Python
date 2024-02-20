from faststream import FastStream
from faststream.rabbit import RabbitBroker
from minio import Minio
from io import BytesIO
from PIL import Image
import pytesseract

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672")
app = FastStream(broker)

minio_bucket = "images"

minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)




@broker.subscriber("ocr")
async def handle(image_name: str):
    print("Received alerts")
    print(image_name)
    objeto = minio_client.get_object(minio_bucket, image_name)
    imagem_bytes = objeto.read()

    imagem = Image.open(BytesIO(imagem_bytes))

    # Extrair texto usando Tesseract
    texto_extraido = pytesseract.image_to_string(imagem)

    # Imprimir o texto extraído
    print(texto_extraido)
