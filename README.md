# DigitalSE 

![DigitalSE](./DigitalSE.jpg)

Version: En

DigitalSE is an open-source document management system designed to deal mainly with old documents digitised in formats such as JPG, PNG and PDF, with the flexibility to adapt to other documents. Its main objective is to ensure simplicity and agility in the document transcription process. This is the version implemented in Python.

## Main features:

1. **Management of Old Documents: The system is specially designed to handle old scanned documents, allowing them to be organised, stored and searched efficiently.

2. **Simplicity and Agility: DigitalSE prioritises ease of use and speed in document transcription, making it accessible and efficient for users.

3. **Microservices Architecture: The system adopts a distributed architecture based on microservices. The leading service receives the document and associated data and stores them in a PostgreSQL database. The image/document is sent to a bucket (e.g. MinIO). However, the system is easily adaptable to integrate with other cloud storage services such as OCI or AWS.

4. **OCR transcription process: The **DigitalSE** uses an optical character recognition (OCR) system to transcribe scanned documents. The image data is sent to a message queue (using RabbitMQ) and processed by the microservice responsible for OCR. This service retrieves the image from the bucket, performs OCR using Tesseract and generates tokens associated with the transcribed content. Subsequently, the transcribed data and tokens are stored in the database for future reference.

## Benefits:

1. **Efficient document management: DigitalSE offers an effective solution for document management, making it easier to organise and quickly access the information contained in digitised documents.

2. **Flexibility and Adaptability**: The system is highly flexible and adaptable to the user's specific needs, with support for a variety of document formats and the ability to integrate with different cloud storage services.

3. **Automating the Transcription Process**: By automating the transcription process through OCR and generating associated tokens, **DigitalSE** reduces the manual workload and speeds up the availability of transcribed information for use.

To summarise, DigitalSE is a comprehensive and efficient document management solution that stands out for its simplicity, agility and ability to integrate with other services and systems.

# Services

**digitalseapi**: This is the main entry point into the system, with the endpoints that communicate with the other services.

**Minio**: File storage service and bucket compatible with cloud storage models.

**Postgres**: A relational database is used to store system data.

# Install


You can [fork](https://github.com/gomesrocha/DigitalSE-OCR-Python/fork) the project if you wish 


1. Clone the project

git clone https://github.com/gomesrocha/DigitalSE-OCR-Python.git

2. Create an .env file with the data for the environment variables in digitalseapi and ocrservice

environment=dev

RABBITMQ_URL=amqp://login:password@server:port/

MINIO_URL=server:port

MINIO_ACCESS_KEY=Access key minio

MINIO_SECRET_KEY=Secret key minio

SECRET_KEY=secret key for auth

DATABASE_URL=postgresql://user:password@server/digitalsedb

MONGODB_URL=mongodb://server:port/


3. To run it, go into the DIgitalSE-OCR-Python project directory and run docker-compose


docker compose up -d --build


4. Check that all the services have been correctly uploaded to the docker

5. Open the project via localhost:8000

Versão: pt-BR

O **DigitalSE** é um sistema de gestão de documentos de código aberto (open-source) projetado para lidar principalmente com documentos antigos digitalizados em formatos como JPG, PNG e PDF, com a flexibilidade para adaptar-se a outros tipos de documentos. Seu principal objetivo é garantir simplicidade e agilidade no processo de transcrição de documentos.  Esta é a versão implementada em Python.

## Características Principais:

1. **Gestão de Documentos Antigos**: O sistema é especialmente projetado para lidar com documentos antigos digitalizados, permitindo sua organização, armazenamento e busca eficientes.

2. **Simplicidade e Agilidade**: O **DigitalSE** prioriza a facilidade de uso e a rapidez no processo de transcrição de documentos, tornando-o acessível e eficiente para os usuários.

3. **Arquitetura de Microsserviços**: O sistema adota uma arquitetura distribuída baseada em microsserviços. O serviço principal recebe o documento e os dados associados, que são então armazenados em um banco de dados PostgreSQL. A imagem/documento é enviada para um bucket (por exemplo, MinIO), embora o sistema seja facilmente adaptável para integrar-se a outros serviços de armazenamento em nuvem, como OCI ou AWS.

4. **Processo de Transcrição por OCR**: O **DigitalSE** utiliza um sistema de reconhecimento óptico de caracteres (OCR) para realizar a transcrição dos documentos digitalizados. Os dados da imagem são enviados para uma fila de mensagens (utilizando RabbitMQ), onde são processados pelo microsserviço responsável pelo OCR. Este serviço recupera a imagem do bucket, executa o OCR usando o Tesseract e gera tokens associados ao conteúdo transcrição. Posteriormente, os dados transcritos e os tokens são armazenados no banco de dados para consulta futura.

## Benefícios:

1. **Eficiência na Gestão de Documentos**: O **DigitalSE** oferece uma solução eficaz para a gestão de documentos, facilitando a organização e o acesso rápido às informações contidas nos documentos digitalizados.

2. **Flexibilidade e Adaptabilidade**: Com suporte para uma variedade de formatos de documentos e a capacidade de integrar-se a diferentes serviços de armazenamento em nuvem, o sistema é altamente flexível e adaptável às necessidades específicas do usuário.

3. **Automatização do Processo de Transcrição**: Ao automatizar o processo de transcrição por meio do OCR e a geração de tokens associados, o **DigitalSE** reduz a carga de trabalho manual e acelera a disponibilidade das informações transcritas para uso.

Em resumo, o **DigitalSE** é uma solução abrangente e eficiente para a gestão de documentos, destacando-se por sua simplicidade, agilidade e capacidade de integração com outros serviços e sistemas.

# Serviços

**digitalseapi**:Principal ponto de entrada no sistema, com os endpoints que realizam a comunicação com os outros serviços.

**Minio**: Serviço de armazenamento de arquivos, bucket compatível com modelos de cloud storage.

**Postgres**: Banco de dados relacional, utilizado para armazenar os dados do sistema.

# Install


Você pode fazer um [fork](https://github.com/gomesrocha/DigitalSE-OCR-Python/fork) do projeto caso desejar 


1. Clone o projeto

git clone https://github.com/gomesrocha/DigitalSE-OCR-Python.git

2. Crie um arquivo .env com os dados das variáveis de ambiente, em digitalseapi e em ocrservice

environment=dev

RABBITMQ_URL=amqp://login:password@server:port/

MINIO_URL=server:port

MINIO_ACCESS_KEY=Access key minio

MINIO_SECRET_KEY=Secret key minio

SECRET_KEY=secret key for auth

DATABASE_URL=postgresql://user:password@server/digitalsedb

MONGODB_URL=mongodb://server:port/

3. Para rodar, entre no diretório do projeto DigitalSE-OCR-Python e execute o docker-compose

docker compose up -d --build


4. Verifique se todos os serviços subiram corretamente no docker

5. Abra o projeto via localhost:8000

