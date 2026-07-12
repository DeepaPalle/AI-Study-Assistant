import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# ---------------------------------------------------------
# Embedding Model
# ---------------------------------------------------------

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ---------------------------------------------------------
# Gemini LLM
# ---------------------------------------------------------

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY,
    temperature=0.3
)

# ---------------------------------------------------------
# Vector Database Location
# ---------------------------------------------------------

DB_DIR = "chroma_db"

# ---------------------------------------------------------
# Create Vector Database
# ---------------------------------------------------------

import shutil

def create_vector_db(pdf_path):

    # Delete old vector database
    if os.path.exists(DB_DIR):
        shutil.rmtree(DB_DIR)

    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    print(f"Pages loaded: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=300
    )

    chunks = splitter.split_documents(documents)

    print(f"Chunks created: {len(chunks)}")

    vectordb = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_DIR
    )

    vectordb.persist()   

    return vectordb

# ---------------------------------------------------------
# Load Existing Vector Database
# ---------------------------------------------------------

def load_vector_db():

    return Chroma(
        persist_directory=DB_DIR,
        embedding_function=embeddings
    )

def get_all_chunks():

    vectordb = load_vector_db()

    data = vectordb.get()

    print("Chunks in DB:", len(data["documents"]))

    print("First chunk:")
    print(data["documents"][0][:500])

    print("Last chunk:")
    print(data["documents"][-1][:500])

    return data["documents"]
# ---------------------------------------------------------
# Ask Question
# ---------------------------------------------------------

def ask_question(question):

    vectordb = load_vector_db()

    retriever = vectordb.as_retriever(
        search_kwargs={"k":10}
    )

    docs = retriever.invoke(question)

    context = "\n\n".join(
        [doc.page_content for doc in docs]
    )

    pages = sorted(
        list(
            set(
                [
                    doc.metadata.get("page",0)+1
                    for doc in docs
                ]
            )
        )
    )

    prompt = f"""
You are an AI Study Assistant.

Answer ONLY from the given context.

If the answer is not available, say

"I couldn't find this information in the uploaded document."

Context:

{context}

Question:

{question}

Answer:
"""

    response = llm.invoke(prompt)

    answer = response.content

    answer += f"\n\n📖 Source Pages : {pages}"

    return answer


# ---------------------------------------------------------
# Get Complete PDF Text
# ---------------------------------------------------------

def get_full_document():

    vectordb = load_vector_db()

    data = vectordb.get()

    documents = data["documents"]

    text = "\n\n".join(documents)

    return text

# ---------------------------------------------------------
# Generate Summary
# ---------------------------------------------------------

def summarize_pdf():

    documents = get_all_chunks()

    batch_size = 50
    summaries = []

    for i in range(0, len(documents), batch_size):

        batch = "\n\n".join(documents[i:i+batch_size])

        prompt = f"""
Summarize the following study material.

Include:
- Main Topics
- Important Concepts
- Key Points

Material:

{batch}
"""

        response = llm.invoke(prompt)
        summaries.append(response.content)

    final_prompt = f"""
Below are summaries of different parts of one PDF.

Create ONE final comprehensive summary.

Include:

1. Overview
2. Main Topics
3. Important Concepts
4. Key Points
5. Interview Preparation

Summaries:

{chr(10).join(summaries)}
"""

    final = llm.invoke(final_prompt)

    return final.content

# ---------------------------------------------------------
# Generate Quiz
# ---------------------------------------------------------

def generate_quiz():

    documents = get_all_chunks()

    batch_size = 50
    quizzes = []

    for i in range(0, len(documents), batch_size):

        batch = "\n\n".join(documents[i:i + batch_size])

        prompt = f"""
You are an AI Study Assistant.

Generate ONLY 3 high-quality Multiple Choice Questions
from the following study material.

Format:

Question:

A)

B)

C)

D)

Correct Answer:

Material:

{batch}
"""

        response = llm.invoke(prompt)

        quizzes.append(response.content)

    final_prompt = f"""
Below are MCQs generated from different sections of one PDF.

Combine them into a single quiz.

Requirements:
- Remove duplicate questions.
- Keep the best questions.
- Return exactly 20 MCQs.

MCQs:

{chr(10).join(quizzes)}
"""

    final_response = llm.invoke(final_prompt)

    return final_response.content
# ---------------------------------------------------------
# Generate Flashcards
# ---------------------------------------------------------

def generate_flashcards():

    documents = get_all_chunks()

    batch_size = 50
    flashcards = []

    for i in range(0, len(documents), batch_size):

        batch = "\n\n".join(documents[i:i + batch_size])

        prompt = f"""
You are an AI Study Assistant.

Generate ONLY 5 flashcards from the following material.

Format:

Question:
Answer:

Material:

{batch}
"""

        response = llm.invoke(prompt)

        flashcards.append(response.content)

    final_prompt = f"""
Below are flashcards generated from different sections of one PDF.

Merge them into one complete flashcard set.

Requirements:
- Remove duplicates.
- Keep the best flashcards.
- Return exactly 50 flashcards.

Flashcards:

{chr(10).join(flashcards)}
"""

    final_response = llm.invoke(final_prompt)

    return final_response.content

