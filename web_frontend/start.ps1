# NoteHub Frontend - Docker Startup Script
# Запуск фронтенда в Docker контейнере

Write-Host "🚀 Starting NoteHub Frontend..." -ForegroundColor Green

# Переход в директорию фронтенда
$frontendPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $frontendPath

# Остановка старых контейнеров
Write-Host "🛑 Stopping old containers..." -ForegroundColor Yellow
docker compose down

# Сборка и запуск
Write-Host "🔨 Building and starting frontend..." -ForegroundColor Cyan
docker compose up --build

Write-Host "✅ Frontend started!" -ForegroundColor Green
Write-Host "🌐 Open: http://localhost:5173" -ForegroundColor Magenta
