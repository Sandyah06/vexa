# Stop any running Ollama
taskkill /IM ollama.exe /F /T 2>$null
Start-Sleep -Seconds 3

# Set environment variables for CPU-only mode
$env:OLLAMA_NUM_GPU = "0"
$env:CUDA_VISIBLE_DEVICES = ""
$env:HIP_VISIBLE_DEVICES = ""

# Start Ollama
Write-Host "🚀 Starting Ollama in CPU-only mode..."
Write-Host "📊 OLLAMA_NUM_GPU = 0 (CPU ONLY)"
ollama serve
