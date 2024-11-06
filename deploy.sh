#!/bin/bash

# Set project directory
PROJECT_DIR=~/Documents/vjt/hexray/practice/CI-CD
LOGDIR=$PROJECT_DIR/logs
LOGFILE=$LOGDIR/deploy.log

# Create directories with proper permissions
create_log_dir() {
    if [ ! -d "$LOGDIR" ]; then
        mkdir -p "$LOGDIR"
        chmod 755 "$LOGDIR"
    fi
    
    if [ ! -f "$LOGFILE" ]; then
        touch "$LOGFILE"
        chmod 644 "$LOGFILE"
    fi
}

# Log function with error handling
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOGFILE" 2>/dev/null || echo "Warning: Could not write to log file"
}

# Ensure proper setup
create_log_dir

# Start deployment
log "Starting deployment"

# Navigate to project directory
cd "$PROJECT_DIR" || {
    log "Error: Could not change to project directory"
    exit 1
}

# Pull latest image
log "Pulling latest image"
docker-compose pull

# Restart container
log "Restarting container"
docker-compose down
docker-compose up -d

# Check container status
log "Checking container status"
docker ps | grep streamlit >> "$LOGFILE" 2>/dev/null

# Clean up old images
log "Cleaning up old images"
docker image prune -f

# Log completion
log "Deployment completed"

# Show container logs
log "Container logs:"
docker-compose logs --tail=20 streamlit >> "$LOGFILE" 2>/dev/null