FROM python:3.13-slim

LABEL org.opencontainers.image.title="student-ml-api"
LABEL org.opencontainers.image.description="Student ML API for MLOps CI/CD assignment"
LABEL org.opencontainers.image.source="https://github.com/zarnab123/student-ml-api"
LABEL org.opencontainers.image.version="1.1.0"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]