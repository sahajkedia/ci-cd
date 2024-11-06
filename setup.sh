#!/bin/bash

# setup.sh
PROJECT_DIR=~/Documents/vjt/hexray/practice/CI-CD

# Create necessary directories
mkdir -p "$PROJECT_DIR/logs"

# Set proper permissions
chmod 755 "$PROJECT_DIR/logs"
touch "$PROJECT_DIR/logs/.gitkeep"
chmod 644 "$PROJECT_DIR/logs/.gitkeep"

# Ensure proper ownership
sudo chown -R $(whoami):$(whoami) "$PROJECT_DIR/logs"

echo "Setup completed successfully"