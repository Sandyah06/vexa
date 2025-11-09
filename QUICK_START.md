
# ⚡ QUICK REFERENCE

## 🚀 STARTUP (Every Time)

### Terminal 1 - Ollama
```powershell
$env:OLLAMA_NUM_GPU = "0"
ollama serve
```

### Terminal 2 - Flask
```powershell
$env:OLLAMA_NUM_GPU = "0"
cd C:\Users\KAVITHA\OneDrive\Desktop\san\vexa
python app.py
```

### Browser
```
http://localhost:5000
```

---

## 📖 ONE MINUTE EXPLANATION

**When you ask "Who is Raju?":**

1. **Convert to numbers:** Question becomes 768 numbers
2. **Search database:** Find most similar document chunks
3. **Get context:** Retrieve 5 most relevant chunks
4. **Ask LLM:** "Read this context, who is Raju?"
5. **Get answer:** LLM generates response
6. **Display:** Answer appears in browser

**Result:** Accurate, context-based answer! ✅

---

## 📚 SIMPLE EXAMPLE

### Upload Story about Raju
```
Action: Click "Ingest Documents"
Input:  C:\Users\KAVITHA\OneDrive\Desktop\san\story\
Result: ✅ Successfully ingested 2 chunks!
```

### Ask Question
```
Action: Type question
Input:  "Who is Raju?"
Result: "Raju is a clever little rabbit..."
```

---

## 🎯 TECHNOLOGY STACK

| Layer | Technology | Location |
|-------|-----------|----------|
| **LLM** | Ollama tinyllama | Local (CPU) |
| **Embeddings** | Ollama nomic-embed-text | Local (CPU) |
| **Database** | Pinecone | Cloud |
| **Web Server** | Flask | Local |
| **UI** | HTML + JavaScript | Browser |

---

## ✅ SYSTEM STATUS

- ✅ Ollama running in CPU mode
- ✅ Embeddings working (Ollama)
- ✅ Pinecone connected
- ✅ Flask serving web UI
- ✅ Documents ingesting
- ✅ Questions answering

---

## 🆘 QUICK FIXES

**"Connection Failed"**
→ Make sure Ollama (Terminal 1) is running first

**"Model memory error"**
→ Already using tinyllama (smallest)
→ Set `$env:OLLAMA_NUM_GPU = "0"` in Terminal 1

**"No documents found"**
→ Ingest documents first using web UI
→ Then ask questions

---

## 📊 PERFORMANCE

- **Upload docs:** 10-30 sec
- **Per query:** 30-60 sec (CPU mode)
- **Database search:** <100ms
- **Model loading:** ~10 sec

---

## 🗂️ PROJECT FILES (11 TOTAL)

```
.venv/                  Virtual environment
.env                    Configuration
app.py                  Flask server (main)
config.py               Load variables
embeddings.py           Ollama embeddings
ingestor_simple.py      Upload documents
query_simple.py         Answer questions
requirements.txt        Dependencies
templates/index.html    Web UI
README.md               Full docs
HOW_IT_WORKS.md         Detailed explanation
```

---

## 💡 HOW EMBEDDINGS HELP

**Without:** Only finds exact word matches
**With:** Understands meaning and context

Example:
- Q: "Who is Raju?"
- Without embeddings: Only finds documents with word "Raju"
- With embeddings: Also finds "the rabbit", "clever animal", etc.

---

## 🔧 CONFIGURE

Edit `.env`:
```env
PINECONE_API_KEY=your_key_here
PINECONE_ENV=us-east-1
PINECONE_INDEX_NAME=vexa
VECTOR_DIM=768
LLM_MODEL=tinyllama
```

---

## 📝 SUPPORTED FILE TYPES

✅ PDF (.pdf)
✅ Text (.txt)
✅ Markdown (.md)

---

## 🎯 3-STEP PROCESS

```
1. UPLOAD DOCUMENTS
   Folder → Split → Embed → Store

2. ASK QUESTION
   Question → Embed → Search → Retrieve

3. GET ANSWER
   Context → LLM → Generate → Display
```

---

## ✨ KEY FEATURES

- ✅ **Local:** Everything runs on your machine
- ✅ **Private:** No external APIs (except Pinecone cloud)
- ✅ **Free:** No OpenAI/paid APIs
- ✅ **Fast:** Optimized for CPU
- ✅ **Smart:** Semantic search understands meaning
- ✅ **Simple:** Clean, minimal codebase

---

**Ready to use! Open http://localhost:5000** 🚀
