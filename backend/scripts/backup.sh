#!/bin/bash
# 智农粮 每日数据库备份脚本
BACKUP_DIR="/data/backup"
DB_USER="znl"
DB_PASSWORD="znl123"
DB_NAME="znl_db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/znl_${TIMESTAMP}.sql"

PGPASSWORD="${DB_PASSWORD}" pg_dump -U "${DB_USER}" -h localhost "${DB_NAME}" > "${FILENAME}"

# 保留最近30天的备份
find "${BACKUP_DIR}" -name "znl_*.sql" -mtime +30 -delete

echo "Backup saved: ${FILENAME}"
