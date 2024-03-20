# Build the app image
FROM python:3.10-slim

# Create directory for the app user
RUN mkdir -p /home/app

# Create the app user
RUN groupadd app && useradd -g app app

# Create the home directory
ENV APP_HOME=/home/app/api
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# install
COPY . $APP_HOME
RUN apt-get update \
  && apt-get -y install --no-install-recommends gcc tesseract-ocr \
  && apt-get clean
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

RUN chown -R app:app $APP_HOME
USER app

CMD ["faststream","run","app:app"]
