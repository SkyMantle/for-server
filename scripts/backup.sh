#!/bin/bash
# Backup script

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.tar.gz"

mkdir -p $BACKUP_DIR

echo "Creating backup..."
tar -czf $BACKUP_FILE \
    --exclude='backups' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.cache' \
    .

echo "Backup created: $BACKUP_FILE"
echo "Size: $(du -h $BACKUP_FILE | cut -f1)"

# Keep only last 5 backups
ls -t $BACKUP_DIR/backup_*.tar.gz | tail -n +6 | xargs -r rm

echo "Old backups cleaned up"
