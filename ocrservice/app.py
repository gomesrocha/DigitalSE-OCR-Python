from faststream import FastStream
from faststream.rabbit import RabbitBroker

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672")
app = FastStream(broker)




@broker.subscriber("ocr")
async def handle(image_name: str):
    print("Received alerts")
    print(image_name)
