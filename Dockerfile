# Use official Python 3.13 image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy dependency file first (better for caching)
COPY requirements.txt .

# Install system dependencies (for SQLAlchemy + Celery + Redis client)
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Expose Flask port
EXPOSE 5000

# Default command (overridden by docker-compose)
CMD ["python", "-m", "messaging.app"]
