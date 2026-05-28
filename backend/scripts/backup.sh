#!/bin/bash
# 智农粮 每日数据库备份脚本
BACKUP_DIR="/data/backup"
DB_USER="root"
DB_PASSWORD="root"
DB_NAME="znl_db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
FILENAME="${BACKUP_DIR}/znl_${TIMESTAMP}.sql"

mysqldump -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" > "${FILENAME}"

# 保留最近30天的备份
find "${BACKUP_DIR}" -name "znl_*.sql" -mtime +30 -delete

echo "Backup saved: ${FILENAME}"
