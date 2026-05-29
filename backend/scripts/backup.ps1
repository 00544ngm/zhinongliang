$ErrorActionPreference = "Stop"

$pgBin = "D:\postsql\postgresql-18.4-1-windows-x64-binaries\pgsql\bin"
$backupDir = "D:\postsql\backup"
$dbHost = "127.0.0.1"
$dbPort = "5432"
$dbUser = "znl"
$dbPassword = "znl123"
$dbName = "znl_db"
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupFile = Join-Path $backupDir "znl_$timestamp.sql"

New-Item -ItemType Directory -Force -Path $backupDir | Out-Null

$env:PGPASSWORD = $dbPassword
try {
  & "$pgBin\pg_dump.exe" -h $dbHost -p $dbPort -U $dbUser -d $dbName -f $backupFile
}
finally {
  Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}

Get-ChildItem -Path $backupDir -Filter "znl_*.sql" |
  Where-Object { $_.LastWriteTime -lt (Get-Date).AddDays(-30) } |
  Remove-Item -Force

Write-Host "Backup saved: $backupFile"
