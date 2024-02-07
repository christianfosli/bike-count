FROM python:3.12-slim

WORKDIR /app
RUN apt-get update && apt-get install -y build-essential software-properties-common && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY bike_count.py .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "bike_count.py", "--server.port=8501", "--server.address=0.0.0.0"]
