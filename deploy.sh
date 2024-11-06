#!/bin/bash

# Set project directory
PROJECT_DIR=~/Documents/vjt/hexray/practice/CI-CD
LOGDIR=$PROJECT_DIR/logs
LOGFILE=$LOGDIR/deploy.log
GITHUB_REPOSITORY="sahajkedia/ci-cd"

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

# Save the current image digest for rollback if needed
save_image_digest() {
    CURRENT_DIGEST=$(docker inspect --format='{{index .RepoDigests 0}}' "ghcr.io/${GITHUB_REPOSITORY}:latest")
    echo "$CURRENT_DIGEST" > "$PROJECT_DIR/.last_stable_image"
    log "Saved current image digest: $CURRENT_DIGEST"
}

# Rollback to the previous version if deployment fails
rollback() {
    if [ -f "$PROJECT_DIR/.last_stable_image" ]; then
        LAST_STABLE_IMAGE=$(cat "$PROJECT_DIR/.last_stable_image")
        log "Rolling back to last stable image: $LAST_STABLE_IMAGE"
        docker-compose down
        docker pull "$LAST_STABLE_IMAGE"
        docker tag "$LAST_STABLE_IMAGE" "ghcr.io/${GITHUB_REPOSITORY}:latest"
        docker-compose up -d
    else
        log "No previous stable image found for rollback"
    fi
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

# Save current image digest before pulling new one
save_image_digest

# Pull latest image
log "Pulling latest image"
if ! docker-compose pull; then
    log "Error: Failed to pull latest image"
    exit 1
fi

# Restart container
log "Restarting container"
docker-compose down
if ! docker-compose up -d; then
    log "Error: Failed to start new container"
    rollback
    exit 1
fi

# Check container status
log "Checking container status"
if ! docker ps | grep streamlit >> "$LOGFILE" 2>/dev/null; then
    log "Error: Container not running after deployment"
    rollback
    exit 1
fi

# Wait for health check
log "Waiting for health check"
sleep 30
if ! curl -s http://localhost:8501/_stcore/health > /dev/null; then
    log "Error: Health check failed"
    rollback
    exit 1
fi

# Clean up old images
log "Cleaning up old images"
docker image prune -f

# Log completion
log "Deployment completed successfully"

# Show container logs
log "Container logs:"
docker-compose logs --tail=20 streamlit >> "$LOGFILE" 2>/dev/null