FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN mkdir -p /vol/web/static

ENV PYTHONUNBUFFERED=1

RUN python manage.py migrate

EXPOSE 8000

CMD ["gunicorn", "skillhub.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]
