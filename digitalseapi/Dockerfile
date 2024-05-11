FROM python:3.13.0b1-slim

# Create directory for the app user
RUN mkdir -p /home/app
RUN mkdir -p /home/app/images
VOLUME /home/app/images
COPY ./app/.env .

# Create the home directory
ENV APP_HOME=/home/app/api
RUN mkdir -p "$APP_HOME"
WORKDIR $APP_HOME
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install
RUN pip 
COPY . $APP_HOME
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt



CMD ["uvicorn","app.main:app","--host=0.0.0.0","--port=8000","--reload"]
