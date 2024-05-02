FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bike_count.py .

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "bike_count.py", "--server.port=8501", "--server.address=0.0.0.0"]
