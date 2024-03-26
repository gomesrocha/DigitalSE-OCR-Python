import aio_pika
from app.infra.config import settings

async def send_data_queue(message_body):
    connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key="ocr",
        )
    # Fechar a conexão
    await connection.close()
