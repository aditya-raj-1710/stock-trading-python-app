#!/bin/bash

# Convenience script to run Docker commands for the stock ticker application
# Usage: ./docker.sh [command]

DOCKER_DIR="build/docker"

case "$1" in
    "up"|"start")
        echo "Starting Docker container..."
        cd "$DOCKER_DIR" && docker-compose up -d
        ;;
    "down"|"stop")
        echo "Stopping Docker container..."
        cd "$DOCKER_DIR" && docker-compose down
        ;;
    "build")
        echo "Building Docker image..."
        cd "$DOCKER_DIR" && docker-compose build
        ;;
    "logs")
        echo "Viewing Docker logs..."
        cd "$DOCKER_DIR" && docker-compose logs -f
        ;;
    "restart")
        echo "Restarting Docker container..."
        cd "$DOCKER_DIR" && docker-compose down && docker-compose up -d
        ;;
    "status"|"ps")
        echo "Checking Docker container status..."
        cd "$DOCKER_DIR" && docker-compose ps
        ;;
    *)
        echo "Usage: $0 {up|start|down|stop|build|logs|restart|status|ps}"
        echo ""
        echo "Commands:"
        echo "  up/start   - Start the container"
        echo "  down/stop  - Stop the container"
        echo "  build      - Build the Docker image"
        echo "  logs       - View container logs"
        echo "  restart    - Restart the container"
        echo "  status/ps  - Check container status"
        echo ""
        echo "For more detailed instructions, see: build/docker/DOCKER_README.md"
        ;;
esac
