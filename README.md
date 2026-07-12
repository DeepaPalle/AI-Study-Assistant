# 🤖 AI Study Assistant using LLM + RAG

An AI-powered Study Assistant that helps students interact with PDF notes using Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG). Users can upload study material, ask questions, generate summaries, quizzes, and flashcards from their documents.

---

## 🚀 Features

- 📄 Upload PDF study materials
- 📚 Create a Knowledge Base using ChromaDB
- 💬 Chat with uploaded PDFs using RAG
- 📖 AI-generated document summaries
- 📝 Automatic quiz generation
- 🗂️ Flashcard generation for quick revision
- 🎯 Semantic search using vector embeddings
- 📑 Displays source pages for answers

---

## 🛠️ Tech Stack

### Frontend
- Streamlit

### Backend
- Python

### AI & LLM
- Google Gemini 2.5 Flash
- LangChain

### Vector Database
- ChromaDB

### Embedding Model
- Hugging Face
- sentence-transformers/all-MiniLM-L6-v2

### PDF Processing
- PyPDFLoader
- RecursiveCharacterTextSplitter

---

## 📂 Project Structure

```
AI-Study-Assistant/
│
├── app.py                  # Streamlit Application
├── rag.py                  # RAG Pipeline
├── requirements.txt
├── .env                    # Google API Key
├── chroma_db/              # Vector Database
├── uploads/                # Uploaded PDFs
├── README.md
└── assets/
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Study-Assistant.git

cd AI-Study-Assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux/Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file.

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
```

Get your API Key from:

https://aistudio.google.com/

---

## ▶️ Run the Project

```bash
streamlit run app.py
```

The application will be available at:

```
http://localhost:8501
```

---

## 📖 How It Works

1. Upload a PDF document.
2. The document is split into chunks.
3. Hugging Face embeddings are generated.
4. Chunks are stored in ChromaDB.
5. User questions retrieve the most relevant chunks.
6. Gemini 2.5 Flash generates answers using the retrieved context.
7. Users can also generate:
   - Summaries
   - Quizzes
   - Flashcards

---

## 🧠 RAG Pipeline

```
PDF
   │
   ▼
PyPDFLoader
   │
   ▼
Text Splitter
   │
   ▼
Embeddings
   │
   ▼
ChromaDB
   │
   ▼
Retriever
   │
   ▼
Gemini 2.5 Flash
   │
   ▼
Answer / Summary / Quiz / Flashcards
```

---


## 👩‍💻 Author

**Deepa Palle**

- GitHub: https://github.com/DeepaPalle
- LinkedIn: https://linkedin.com/in/deepa-palle

---
