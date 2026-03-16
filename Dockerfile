FROM python:3.11-slim

WORKDIR /app

RUN git config --system --add safe.directory /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
