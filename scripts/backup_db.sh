#!/bin/bash

# Thiết lập các biến
BACKUP_DIR="database_backups"
DATE=$(date +%Y-%m-%d)
BACKUP_FILE="$BACKUP_DIR/backup_$DATE.sql"
DAYS_TO_KEEP=7

# Tạo thư mục backup nếu chưa tồn tại
mkdir -p "$BACKUP_DIR"

# Backup database
docker compose -f docker/prod/docker-compose.yml exec -T db pg_dump -U postgres > "$BACKUP_FILE"

# Nén file backup
gzip -f "$BACKUP_FILE"

# Xóa các file backup cũ hơn 7 ngày
find "$BACKUP_DIR" -name "backup_*.sql.gz" -type f -mtime +$DAYS_TO_KEEP -delete

echo "Database backup completed: $BACKUP_FILE.gz"

# Kiểm tra kết quả backup
if [ -f "$BACKUP_FILE.gz" ]; then
    echo "Backup size: $(du -h "$BACKUP_FILE.gz" | cut -f1)"
else
    echo "Backup failed!"
    exit 1
fi