# DigitalSE-OCR-Python

O **DigitalSE** é um sistema de gestão de documentos de código aberto (open-source) projetado para lidar principalmente com documentos antigos digitalizados em formatos como JPG, PNG e PDF, com a flexibilidade para adaptar-se a outros tipos de documentos. Seu principal objetivo é garantir simplicidade e agilidade no processo de transcrição de documentos.

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


'''

git clone https://github.com/gomesrocha/DigitalSE-OCR-Python.git

'''

2. Para rodar, entre no diretório do projeto DIgitalSE-OCR-Python e execute o docker-compose

'''

docker compose up -d --build

'''

3. Verifique se todos os serviços subiram corretamente no docker

4. Abra o projeto via localhost:8000

