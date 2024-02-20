# Build the app image
FROM python:3.10-slim

# Create directory for the app user
RUN mkdir -p /home/app
RUN mkdir -p /home/app/images
VOLUME /home/app/images

# Create the home directory
ENV APP_HOME=/home/app/api
RUN mkdir -p "$APP_HOME"
WORKDIR $APP_HOME
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install
COPY . $APP_HOME
RUN pip install --no-cache-dir -r requirements.txt
RUN opentelemetry-bootstrap -a install


CMD ["opentelemetry-instrument","uvicorn","app.main:app","--host=0.0.0.0","--port=8000","--reload"]
