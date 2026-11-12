FROM python:3.11-slim
RUN apt-get update && apt-get install -y openjdk-17-jre-headless && rm -rf /var/lib/apt/lists/*
WORKDIR /opt/project
COPY requirements.txt .
RUN grep -v airflow requirements.txt | pip install --no-cache-dir -r /dev/stdin
COPY . .
CMD ["python", "-m", "src.main", "--stage", "all"]
