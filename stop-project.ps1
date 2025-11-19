# Vai para a pasta infra
Write-Host "🔹 Entrando na pasta infra..."
Set-Location "$PSScriptRoot\infra"

# Para todos os containers e remove volumes
Write-Host "🛑 Parando containers e removendo volumes..."
docker compose down -v

# Mostra uso de disco antes da limpeza
Write-Host "🔹 Calculando uso de disco antes da limpeza..."
$before = (docker system df)

# Remove imagens não utilizadas
Write-Host "🧹 Limpando imagens não utilizadas..."
docker image prune -a -f

# Remove volumes não utilizados
Write-Host "🧹 Limpando volumes não utilizados..."
docker volume prune -f

# Remove redes não utilizadas
Write-Host "🧹 Limpando redes não utilizadas..."
docker network prune -f

# Mostra uso de disco depois da limpeza
Write-Host "🔹 Calculando uso de disco depois da limpeza..."
$after = (docker system df)

Write-Host "✅ Projeto encerrado e recursos limpos com sucesso."
Write-Host "📊 Resumo do espaço liberado:"
Write-Host "Antes da limpeza:"
$before
Write-Host "Depois da limpeza:"
$after
