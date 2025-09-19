FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir duckdb pandas requests pyarrow

CMD ["python", "etl/etl_pipeline.py"]
