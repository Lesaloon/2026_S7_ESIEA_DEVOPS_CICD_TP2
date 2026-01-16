# Use Python 3.11 slim image (matches CI/CD pipeline)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies (production and development)
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port 8000
EXPOSE 8000

# Set default environment variable for database path
ENV APP_DB_PATH=/data/app.db

# Run the Flask application
CMD ["python", "api.py"]
