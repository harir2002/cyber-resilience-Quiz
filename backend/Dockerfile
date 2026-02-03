# Use official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DATA_DIR=/data

# Create the data directory (for Hugging Face Persistent Storage)
# Hugging Face usually mounts the persistent volume at /data
RUN mkdir -p /data

# Install system dependencies (needed for some Python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user (Hugging Face strict security)
# HF Spaces run as user 1000 by default
RUN useradd -m -u 1000 user
RUN chown -R user:user /app /data
USER user

# Expose port 7860 (Standard Hugging Face Space port)
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
