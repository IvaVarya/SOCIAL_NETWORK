#Dockerfile
FROM python:3.9-slim

# Установка postgresql-client
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Скопируйте wait-for-postgres.sh и сделайте его исполняемым
COPY wait-for-postgres.sh /wait-for-postgres.sh
RUN chmod +x /wait-for-postgres.sh

EXPOSE 5002

CMD ["python", "app.py"]