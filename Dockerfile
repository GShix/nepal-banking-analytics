# Use official lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files
# and ensure logs appear immediately
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Make the src directory available for Python imports
ENV PYTHONPATH=/workspace/src

# Set container working directory
WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency file first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ ./src/

# Copy data directory
COPY data/ ./data/

# Run the end-to-end banking analytics pipeline
CMD ["python", "src/main.py"]