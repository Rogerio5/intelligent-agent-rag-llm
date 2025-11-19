# Ativa o ambiente virtual
Write-Host "🔹 Ativando ambiente virtual..."
& "$PSScriptRoot\.venv\Scripts\Activate.ps1"

# Verifica se o Docker Engine está rodando
Write-Host "🔹 Verificando Docker Engine..."
$dockerInfo = docker info 2>&1

if ($dockerInfo -match "Server Version") {
    Write-Host "✅ Docker Engine está rodando!"
} else {
    Write-Host "❌ Docker Engine não está rodando. Abra o Docker Desktop e tente novamente."
    exit 1
}

# Vai para a pasta infra
Write-Host "🔹 Entrando na pasta infra..."
Set-Location "$PSScriptRoot\infra"

# Sobe os containers em background (detached mode)
Write-Host "🚀 Subindo containers em background..."
docker compose up --build -d

# Abre os serviços no navegador
Write-Host "🔹 Abrindo serviços no navegador..."
Start-Process "http://localhost:8000/docs"      # API FastAPI
Start-Process "http://localhost:5000"           # MLflow
Start-Process "http://localhost:9090"           # Prometheus
Start-Process "http://localhost:3000"           # Grafana

Write-Host "✅ Projeto iniciado com sucesso! Containers rodando em background."
