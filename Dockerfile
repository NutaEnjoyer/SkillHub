FROM python:3.11-slim as builder

WORKDIR /install

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt . 

RUN pip install --upgrade pip && \
    pip wheel --no-deps --wheel-dir /wheels -r requirements.txt --no-cache-dir 

FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1 

WORKDIR /app

COPY --from=builder /wheels /wheels
COPY requirements.txt .

RUN pip install --no-deps --no-index --find-links=/wheels -r requirements.txt && \
    rm -rf /wheels requirements.txt

COPY . .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "skillhub.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4"]

