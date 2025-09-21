# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TZ=Asia/Kolkata

# Install system dependencies
RUN apt-get update && apt-get install -y \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY src/script.py .
COPY src/schedule_ticker_script.py .
#COPY output/tickers.csv .

# Create directory for output files
RUN mkdir -p /app/output

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port (if needed for health checks)
EXPOSE 8000

# Default command - run the scheduled script
CMD ["python", "schedule_ticker_script.py"]
