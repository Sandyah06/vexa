# 🎉 Vexa - Setup Complete!

## System is Ready to Use! 

### **Current Configuration:**

✅ **LLM Model**: `llama3.2` (configured in `.env`)
✅ **Embeddings**: `nomic-embed-text` (768 dimensions)
✅ **Vector DB**: Pinecone (index: `vexa`)
✅ **Mode**: CPU-only (no GPU memory issues)
✅ **UI Theme**: Professional light mode

---

## **How to Start the System:**

### **Terminal 1 - Start Ollama (CPU-only):**
```powershell
cd "c:\Users\KAVITHA\OneDrive\Desktop\san\vexa"
$env:OLLAMA_NUM_GPU = "0"
ollama serve
```

Wait for Ollama to show: `Listening on 127.0.0.1:11434`

### **Terminal 2 - Start Flask:**
```powershell
cd "c:\Users\KAVITHA\OneDrive\Desktop\san\vexa"
python app.py
```

Wait for Flask to show: `Running on http://127.0.0.1:5000`

---

## **Using the System:**

1. **Open Browser**: Go to `http://127.0.0.1:5000`

2. **Upload Documents**:
   - Paste folder path (e.g., `C:\Users\KAVITHA\OneDrive\Desktop\san\story`)
   - Click "Upload"
   - Wait for: `✅ Path read successfully`

3. **Ask Questions**:
   - Type your question in the chat box
   - Press Enter or click Send
   - Get AI-powered answers from your documents!

---

## **Key Features:**

✅ **Auto-Clear**: Pinecone automatically clears between uploads (no contamination)
✅ **Document-Only**: Only answers from your uploaded documents (no hallucination)
✅ **Clean Answers**: No preamble like "The answer is..." - just pure answers
✅ **Smart Length**: Automatically understands if you want brief or detailed answers
✅ **Professional UI**: Modern, light-themed chatbot interface
✅ **Supported Formats**: PDF, TXT, MD files

---

## **Troubleshooting:**

### **Issue: "Failed to connect to Ollama"**
- Make sure Terminal 1 (Ollama) is running and shows `Listening on 127.0.0.1:11434`

### **Issue: "model requires more system memory"**
- Make sure `$env:OLLAMA_NUM_GPU = "0"` is set BEFORE starting Ollama
- Ollama should show `library=cpu` in the logs

### **Issue: Wrong answers from old documents**
- Pinecone auto-clears on each upload - make sure to upload new folder after changing documents

---

## **Project Files:**

- `app.py` - Flask web server
- `query_simple.py` - Question answering with Ollama + Pinecone
- `embeddings.py` - Semantic embeddings (local)
- `ingestor_simple.py` - Document ingestion
- `config.py` - Configuration loader
- `templates/index.html` - Web UI
- `.env` - Environment configuration (Pinecone API key, model names, etc.)

---

## **System Architecture:**

```
User Interface (Browser)
         ↓
    Flask App (5000)
         ↓
   Ollama LLM (11434) + Pinecone Vector DB
         ↓
   Documents → Embeddings → Semantic Search → Answer Generation
```

---

**Enjoy using Vexa! 🚀**
