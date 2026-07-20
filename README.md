# 📚 AI Study Assistant
### AI-Powered PDF Learning Assistant using RAG, LangChain & Google Gemini

An intelligent study assistant that transforms PDF documents into interactive learning material. Users can upload lecture notes, textbooks, or research papers and instantly generate summaries, ask context-aware questions, create quizzes, and build flashcards using Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- 📄 Upload and process PDF documents
- 🤖 Context-aware Question Answering using Retrieval-Augmented Generation (RAG)
- 📝 Automatic document summarization
- ❓ AI-generated Multiple Choice Quizzes
- 🎴 AI-generated Flashcards for revision
- 🔍 Semantic document search with vector embeddings
- 📑 Page-level source citations for generated answers
- 📤 Export summaries, quizzes, and flashcards in TXT or JSON format
- ⚡ Interactive Streamlit web interface

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|--------------|
| Frontend | Streamlit |
| LLM | Google Gemini 2.5 Flash |
| Framework | LangChain |
| Embeddings | HuggingFace Sentence Transformers |
| Vector Database | ChromaDB |
| PDF Processing | PyPDF |
| Language | Python |

---

## 🏗️ Architecture

```
               PDF Upload
                    │
                    ▼
         PDF Text Extraction (PyPDF)
                    │
                    ▼
      Text Chunking (LangChain Splitter)
                    │
                    ▼
      HuggingFace Embeddings Generation
                    │
                    ▼
          ChromaDB Vector Storage
                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼
  RAG Chat      Summarizer     Quiz & Flashcards
      │             │             │
      └─────────────┼─────────────┘
                    ▼
             Streamlit Interface
```

---

## 📂 Project Structure

```
ai_study_assistant/
│
├── app.py
├── requirements.txt
├── .env.example
│
├── src/
│   ├── config.py
│   ├── pdf_processor.py
│   ├── vector_store.py
│   ├── rag_chain.py
│   ├── summarizer.py
│   ├── quiz_generator.py
│   ├── flashcard_generator.py
│   ├── utils.py
│   └── __init__.py
│
└── README.md
```

---

## ⚙️ Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/ai-study-assistant.git

cd ai-study-assistant
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate it:

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

## 🔑 Configure API Key

Create a `.env` file.

```env
GOOGLE_API_KEY=your_api_key_here
```

Get a free API key from

https://aistudio.google.com/app/apikey

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

Open your browser at

```
http://localhost:8501
```

---

## 📸 Workflow

1. Upload a PDF
2. Process the document
3. Ask questions about the content
4. Generate AI summary
5. Create quizzes
6. Generate flashcards
7. Export learning material

---

## 💡 Key Concepts Used

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Embeddings
- Large Language Models (LLMs)
- Prompt Engineering
- Document Chunking
- Dense Retrieval
- Similarity Search

---

## 📈 Resume Highlights

- Built an end-to-end AI-powered study assistant using Retrieval-Augmented Generation (RAG).
- Implemented semantic document search using HuggingFace embeddings and ChromaDB.
- Integrated Google Gemini with LangChain for context-aware question answering.
- Developed automated summarization, quiz generation, and flashcard creation pipelines.
- Designed an interactive Streamlit application for real-time PDF-based learning.

---

## 🔮 Future Enhancements

- Multi-document support
- Chat history persistence
- OCR support for scanned PDFs
- Voice-based question answering
- User authentication
- Cloud deployment (AWS/GCP/Azure)
- Learning progress dashboard

---



