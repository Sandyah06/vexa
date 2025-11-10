@echo off
REM Set Ollama to CPU-only mode before starting
set OLLAMA_NUM_GPU=0
set CUDA_VISIBLE_DEVICES=
set HIP_VISIBLE_DEVICES=
echo Starting Ollama in CPU-only mode...
ollama serve
