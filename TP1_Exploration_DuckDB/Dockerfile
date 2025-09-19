FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir duckdb pandas

CMD ["python", "analysis_duckdb.py"]
