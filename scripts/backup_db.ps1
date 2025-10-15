$date = Get-Date -Format "yyyy-MM-dd"
$backupPath = "database_backups"

# Tạo thư mục backup nếu chưa tồn tại
if (!(Test-Path -Path $backupPath)) {
    New-Item -ItemType Directory -Path $backupPath
}

# Backup database
docker compose -f docker/prod/docker-compose.yml exec -T db pg_dump -U postgres > "$backupPath/backup_$date.sql"

# Xóa các file backup cũ hơn 7 ngày
Get-ChildItem -Path $backupPath -Filter "backup_*.sql" | Where-Object {
    $_.LastWriteTime -lt (Get-Date).AddDays(-7)
} | Remove-Item -Force

Write-Host "Database backup completed: $backupPath/backup_$date.sql"