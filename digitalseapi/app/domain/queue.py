import aio_pika


async def send_data_queue(message_body):
    connection = await aio_pika.connect_robust("amqp://guest:guest@rabbitmq:5672/")
    async with connection:
        channel = await connection.channel()

        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()),
            routing_key="ocr",
        )
    # Fechar a conexão
    await connection.close()
