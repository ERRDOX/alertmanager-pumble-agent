FROM python:3.9-slim

WORKDIR /app

COPY src/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/app.py .

EXPOSE 9094

CMD ["gunicorn", "--bind", "0.0.0.0:9094", "app:app"]