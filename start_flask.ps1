# Start Flask with CPU-only environment
cd "c:\Users\KAVITHA\OneDrive\Desktop\san\vexa"

# Set environment variables
$env:OLLAMA_NUM_GPU = "0"
$env:CUDA_VISIBLE_DEVICES = ""
$env:HIP_VISIBLE_DEVICES = ""

Write-Host "🚀 Starting Flask..."
Write-Host "📊 Using llama3.2 model in CPU-only mode"
Write-Host "🔗 Access at http://127.0.0.1:5000"
Write-Host ""

python app.py
