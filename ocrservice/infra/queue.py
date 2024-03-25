from faststream import FastStream
from faststream.rabbit import RabbitBroker
from minio import Minio

broker = RabbitBroker("amqp://guest:guest@rabbitmq:5672")
app = FastStream(broker)
minio_bucket = "images"
minio_client = Minio("minio:9000",
                      access_key="digitalse",
                      secret_key="digitalse",
                      secure=False)
