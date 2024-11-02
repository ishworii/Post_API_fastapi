FROM python:3.12
WORKDIR /fastapi_server
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY /app ./app
COPY /tests ./tests
COPY /.env.docker .env
EXPOSE 8000
CMD ["fastapi","run","./app/main.py","--port","8000"]