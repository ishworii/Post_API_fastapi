FROM python:3.12
WORKDIR /fastapi_server
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY backend/app /app
COPY backend/.env.docker .env
EXPOSE 8000
CMD ["fastapi","run","/app/main.py","--port","8000"]