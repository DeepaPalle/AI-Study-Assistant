"""
AI Study Assistant — RAG-powered PDF Q&A, summarization, quiz and
flashcard generation.

Stack: Streamlit (UI) + LangChain (orchestration) + Gemini (LLM) +
ChromaDB (vector store) + Hugging Face sentence-transformers (embeddings).

Run with:  streamlit run app.py
"""
import streamlit as st

from src.config import Config
from src.pdf_processor import process_pdf, full_text_from_documents
from src.vector_store import build_vectorstore
from src.rag_chain import ask_question
from src.summarizer import summarize_documents
from src.quiz_generator import generate_quiz
from src.flashcard_generator import generate_flashcards
from src.utils import (
    make_collection_name,
    flashcards_to_text,
    quiz_to_text,
    flashcards_to_json,
    quiz_to_json,
    friendly_error_message,
)

st.set_page_config(page_title="AI Study Assistant", page_icon="📚", layout="wide")

# ---------------------------------------------------------------- session state
defaults = {
    "vectordb": None,
    "doc_chunks": None,
    "doc_name": None,
    "chat_history": [],
    "summary": None,
    "quiz": None,
    "flashcards": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ---------------------------------------------------------------- sidebar
with st.sidebar:
    st.title("📚 AI Study Assistant")
    st.caption("RAG-powered PDF Q&A · Summaries · Quizzes · Flashcards")

    st.subheader("1. Gemini API Key")
    api_key_input = st.text_input(
        "Google Gemini API key",
        value=Config.GOOGLE_API_KEY,
        type="password",
        help="Get a free key at https://aistudio.google.com/app/apikey",
    )
    if api_key_input:
        Config.GOOGLE_API_KEY = api_key_input

    st.subheader("2. Upload a PDF")
    uploaded_file = st.file_uploader("Choose a study PDF", type=["pdf"])

    process_clicked = st.button("Process document", type="primary", use_container_width=True)

    if process_clicked:
        if not Config.is_ready():
            st.error("Please enter your Gemini API key first.")
        elif not uploaded_file:
            st.error("Please upload a PDF first.")
        else:
            with st.spinner("Extracting text, chunking, and embedding..."):
                try:
                    file_bytes = uploaded_file.getvalue()
                    chunks = process_pdf(file_bytes, uploaded_file.name)
                    collection_name = make_collection_name(uploaded_file.name, file_bytes)
                    vectordb = build_vectorstore(chunks, collection_name)

                    st.session_state.vectordb = vectordb
                    st.session_state.doc_chunks = chunks
                    st.session_state.doc_name = uploaded_file.name
                    st.session_state.chat_history = []
                    st.session_state.summary = None
                    st.session_state.quiz = None
                    st.session_state.flashcards = None

                    st.success(f"Processed '{uploaded_file.name}' into {len(chunks)} chunks.")
                except Exception as e:
                    st.error(f"Failed to process PDF: {e}")

    if st.session_state.doc_name:
        st.info(f"📄 Active document:\n**{st.session_state.doc_name}**")

    st.divider()
    st.caption(
        "Embeddings: Hugging Face (local) · LLM: Gemini · "
        "Vector store: ChromaDB · Orchestration: LangChain"
    )

# ---------------------------------------------------------------- main area
st.title("AI Study Assistant")

if not st.session_state.vectordb:
    st.markdown(
        """
        👋 **Welcome!** To get started:
        1. Enter your free Gemini API key in the sidebar.
        2. Upload a PDF (lecture notes, textbook chapter, research paper).
        3. Click **Process document**.

        Then you'll be able to ask questions, get a summary, and
        auto-generate a quiz and flashcards from the material.
        """
    )
    st.stop()

tab_chat, tab_summary, tab_quiz, tab_flashcards = st.tabs(
    ["💬 Ask Questions", "📝 Summary", "🧠 Quiz", "🗂️ Flashcards"]
)

# ---------------------------------------------------------------- Chat / Q&A tab
with tab_chat:
    st.subheader("Ask questions about your document")

    for turn in st.session_state.chat_history:
        with st.chat_message("user"):
            st.write(turn["question"])
        with st.chat_message("assistant"):
            st.write(turn["answer"])
            if turn.get("sources"):
                with st.expander("Sources"):
                    for s in turn["sources"]:
                        st.markdown(f"**Page {s['page']}** — {s['snippet']}")

    question = st.chat_input("Ask something about the document...")
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant"):
            with st.spinner("Retrieving relevant context and thinking..."):
                try:
                    result = ask_question(st.session_state.vectordb, question)
                    st.write(result["answer"])
                    if result["sources"]:
                        with st.expander("Sources"):
                            for s in result["sources"]:
                                st.markdown(f"**Page {s['page']}** — {s['snippet']}")
                    st.session_state.chat_history.append(
                        {"question": question, "answer": result["answer"], "sources": result["sources"]}
                    )
                except Exception as e:
                    st.error(f"Something went wrong: {friendly_error_message(e)}")

# ---------------------------------------------------------------- Summary tab
with tab_summary:
    st.subheader("Document summary")
    col1, col2 = st.columns([1, 3])
    with col1:
        style = st.radio("Summary style", ["detailed", "brief"], index=0)
        if st.button("Generate summary", use_container_width=True):
            with st.spinner("Summarizing document..."):
                try:
                    st.session_state.summary = summarize_documents(
                        st.session_state.doc_chunks, style=style
                    )
                except Exception as e:
                    st.error(f"Failed to summarize: {friendly_error_message(e)}")
    with col2:
        if st.session_state.summary:
            st.markdown(st.session_state.summary)
            st.download_button(
                "Download summary (.txt)",
                st.session_state.summary,
                file_name="summary.txt",
            )
        else:
            st.caption("Click 'Generate summary' to summarize the whole document.")

# ---------------------------------------------------------------- Quiz tab
with tab_quiz:
    st.subheader("Auto-generated quiz")
    num_q = st.slider("Number of questions", 3, 15, 5)
    if st.button("Generate quiz"):
        with st.spinner("Writing quiz questions..."):
            try:
                st.session_state.quiz = generate_quiz(st.session_state.doc_chunks, num_questions=num_q)
                st.session_state["quiz_answers"] = {}
            except Exception as e:
                st.error(f"Failed to generate quiz: {friendly_error_message(e)}")

    if st.session_state.quiz:
        with st.form("quiz_form"):
            user_answers = {}
            for i, q in enumerate(st.session_state.quiz):
                st.markdown(f"**Q{i+1}. ({q.get('difficulty','medium')}) {q['question']}**")
                options = q["options"]
                labels = [f"{k}. {v}" for k, v in options.items()]
                choice = st.radio(
                    f"q_{i}", labels, key=f"quiz_radio_{i}", label_visibility="collapsed"
                )
                user_answers[i] = choice.split(".")[0].strip()
                st.write("")
            submitted = st.form_submit_button("Submit quiz")

        if submitted:
            score = 0
            for i, q in enumerate(st.session_state.quiz):
                correct = q["correct_answer"]
                given = user_answers[i]
                is_correct = given == correct
                score += int(is_correct)
                icon = "✅" if is_correct else "❌"
                st.markdown(
                    f"{icon} **Q{i+1}:** your answer **{given}**, correct answer **{correct}**  \n"
                    f"_{q.get('explanation','')}_"
                )
            st.success(f"Score: {score} / {len(st.session_state.quiz)}")

        st.download_button(
            "Download quiz (.txt)",
            quiz_to_text(st.session_state.quiz),
            file_name="quiz.txt",
        )
        st.download_button(
            "Download quiz (.json)",
            quiz_to_json(st.session_state.quiz),
            file_name="quiz.json",
        )

# ---------------------------------------------------------------- Flashcards tab
with tab_flashcards:
    st.subheader("Flashcards")
    num_cards = st.slider("Number of flashcards", 5, 30, 10)
    if st.button("Generate flashcards"):
        with st.spinner("Creating flashcards..."):
            try:
                st.session_state.flashcards = generate_flashcards(
                    st.session_state.doc_chunks, num_cards=num_cards
                )
            except Exception as e:
                st.error(f"Failed to generate flashcards: {friendly_error_message(e)}")

    if st.session_state.flashcards:
        cols = st.columns(2)
        for i, card in enumerate(st.session_state.flashcards):
            with cols[i % 2]:
                with st.expander(f"🗂️ [{card.get('topic','General')}]  {card['front']}"):
                    st.write(card["back"])

        st.download_button(
            "Download flashcards (.txt)",
            flashcards_to_text(st.session_state.flashcards),
            file_name="flashcards.txt",
        )
        st.download_button(
            "Download flashcards (.json)",
            flashcards_to_json(st.session_state.flashcards),
            file_name="flashcards.json",
        )
