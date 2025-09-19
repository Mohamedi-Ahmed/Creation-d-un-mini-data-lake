FROM python:3.10-slim

WORKDIR /app

COPY app/ app/
COPY data/ data/

RUN pip install streamlit duckdb pandas

EXPOSE 8501

CMD ["streamlit", "run", "app/app.py", "--server.port=8501", "--server.address=0.0.0.0"]