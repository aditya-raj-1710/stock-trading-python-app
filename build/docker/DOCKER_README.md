# Docker Setup for Stock Ticker Application

This Docker setup allows you to run the stock ticker collection script daily at 9 PM IST in a containerized environment.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- Polygon.io API key

## Setup Instructions

### 1. Environment Configuration

Create a `.env` file in the project root (two directories up from this docker folder) with your API key:

```bash
# From the project root directory
cp .env.example .env
```

Edit the `.env` file and add your Polygon.io API key:

```
POLYGON_API_KEY=your_actual_api_key_here
```

### 2. Build and Run with Docker Compose

```bash
# Navigate to the docker directory
cd build/docker

# Build and start the container
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the container
docker-compose down
```

**Note**: The Docker build context is set to the project root, so all files are accessible from the Dockerfile.

### 3. Manual Docker Commands

If you prefer to use Docker directly:

```bash
# Build the image from project root
docker build -f build/docker/Dockerfile -t stock-ticker-app .

# Run the container
docker run -d \
  --name stock-ticker-scheduler \
  --env-file .env \
  -v $(pwd)/output:/app/output \
  -v $(pwd)/logs:/app/logs \
  stock-ticker-app

# View logs
docker logs -f stock-ticker-scheduler

# Stop and remove container
docker stop stock-ticker-scheduler
docker rm stock-ticker-scheduler
```

## Features

- **Scheduled Execution**: Runs daily at 9:00 PM IST
- **Health Monitoring**: Basic job runs every minute for health checks
- **Comprehensive Logging**: 
  - Detailed execution logs with timestamps
  - Progress tracking (page count, total tickers)
  - API error handling and validation
  - File operations and size monitoring
  - Multiple log levels (INFO, ERROR, WARNING, DEBUG)
- **Data Persistence**: CSV output files are saved to the `output/` directory
- **Error Handling**: Robust error handling with detailed logging and graceful failures
- **Rate Limiting**: Built-in delays to respect API limits

## File Structure

```
├── build/
│   └── docker/
│       ├── Dockerfile                 # Docker image configuration
│       ├── docker-compose.yml        # Docker Compose configuration
│       ├── .dockerignore            # Files to exclude from Docker build
│       └── DOCKER_README.md         # This documentation
├── src/
│   ├── __init__.py                   # Python package marker
│   ├── script.py                     # Main ticker collection script
│   └── schedule_ticker_script.py     # Scheduler script
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── output/                  # Directory for CSV output files
└── logs/                    # Directory for log files
```

## Monitoring

### View Logs

```bash
# Real-time container logs
docker-compose logs -f

# View scheduler logs
tail -f logs/scheduler.log

# View ticker fetch logs
tail -f logs/ticker_fetch.log

# Search for errors across all logs
grep -i error logs/*.log

# View recent log entries
tail -n 50 logs/ticker_fetch.log
```

### Check Container Status

```bash
# Check if container is running
docker-compose ps

# View container details
docker-compose exec stock-ticker-app ps aux
```

## Output Files

- **CSV Data**: `output/tickers.csv` - Contains the collected ticker data
- **Logs**: 
  - `logs/scheduler.log` - Scheduler and container health logs
  - `logs/ticker_fetch.log` - Detailed ticker data collection logs

## Troubleshooting

### Container Won't Start

1. Check if your `.env` file exists and has the correct API key
2. Verify Docker is running: `docker --version`
3. Check logs: `docker-compose logs`

### No Data Collection

1. Verify your Polygon.io API key is valid
2. Check network connectivity
3. Review logs for error messages:
   ```bash
   # Check for API errors
   grep -i "error\|failed" logs/ticker_fetch.log
   
   # Check for network issues
   grep -i "timeout\|connection" logs/ticker_fetch.log
   
   # View recent execution logs
   tail -n 100 logs/ticker_fetch.log
   ```
4. Verify the scheduler is running:
   ```bash
   # Check scheduler logs
   tail -f logs/scheduler.log
   ```

### Time Zone Issues

The container is configured to use IST (Asia/Kolkata) timezone. If you need a different timezone, modify the `TZ` environment variable in `docker-compose.yml`.

## Stopping the Service

```bash
# Stop the container
docker-compose down

# Stop and remove volumes (if needed)
docker-compose down -v
```

## Updating the Application

1. Make your code changes
2. Navigate to the docker directory: `cd build/docker`
3. Rebuild the image: `docker-compose build`
4. Restart the container: `docker-compose up -d`
