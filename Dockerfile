# Use official lightweight Python base image
FROM python:3.11-slim

# Prevent Python from writing .pyc files & buffer stdout/stderr for quick logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set container working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies list and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and project directories
COPY app/ ./app/
COPY src/ ./src/
COPY data/ ./data/
COPY notebooks/ ./notebooks/

# Expose Streamlit's default port
EXPOSE 8501

# Default startup command launches the Streamlit Dashboard
CMD ["streamlit", "run", "app/dashboard.py", "--server.port=8501", "--server.address=0.0.0.0"]