# DigitalSE-OCR-Python
Nova versão do DigitalSE usando Python, Tesseract OCR, FastAPI, MINIO, RabbitMQ e distribuido com microsserviços.

# Serviços
## digitalseapi
Principal ponto de entrada no sistema, com os endpoints que realizam a comunicação com os outros serviços.

## Minio
Serviço de armazenamento de arquivos, bucket compatível com modelos de cloud storage.

## Postgres
Banco de dados relacional, utilizado para armazenar os dados do sistema.
