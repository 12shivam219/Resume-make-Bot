# Base image with Python and LibreOffice
FROM python:3.9-slim as base

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV LIBREOFFICE_HOME=/usr/lib/libreoffice
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

# Create and set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create uploads directory
RUN mkdir -p /app/uploads && chmod 777 /app/uploads

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "run:app"]