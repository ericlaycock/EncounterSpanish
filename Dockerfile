FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create audio directory for TTS files
RUN mkdir -p /tmp/audio

# Expose port
EXPOSE 8000

# Copy startup script
COPY start.py /start.py
RUN chmod +x /start.py

# Run the application
CMD ["python", "/start.py"]



