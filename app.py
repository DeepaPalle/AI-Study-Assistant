import streamlit as st
import os

from rag import (
    create_vector_db,
    ask_question,
    summarize_pdf,
    generate_quiz,
    generate_flashcards,
)

# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "db_created" not in st.session_state:
    st.session_state.db_created = False

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    color:#4CAF50;
    font-size:42px;
    font-weight:bold;
}

.subtitle{
    text-align:center;
    color:gray;
    font-size:18px;
}

.stButton>button{
    width:100%;
    border-radius:10px;
    height:45px;
    font-size:16px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------

st.markdown(
    "<p class='main-title'>🤖 AI Study Assistant using LLM + RAG</p>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p class='subtitle'>Upload your PDF and interact with it using AI.</p>",
    unsafe_allow_html=True,
)

# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("📚 AI Study Assistant")



st.sidebar.metric(
    "Questions Asked",
    len(st.session_state.chat_history)
)

# -----------------------------
# Upload PDF
# -----------------------------

uploaded_file = st.file_uploader(
    "📄 Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully!")

    if st.button("Create Knowledge Base"):

        with st.spinner("Creating Vector Database..."):

            create_vector_db(pdf_path)

        st.session_state.db_created = True

        st.success("Knowledge Base Created Successfully!")

st.divider()
# -----------------------------
# Tabs
# -----------------------------

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "💬 Chat",
        "📄 Summary",
        "📝 Quiz",
        "🗂 Flashcards",
    ]
)

# ======================================================
# Chat Tab
# ======================================================

with tab1:

    if st.session_state.db_created:

        st.header("💬 Chat with your PDF")

        question = st.chat_input(
            "Ask anything about your uploaded PDF..."
        )

        if question:

            with st.spinner("Thinking..."):

                answer = ask_question(question)

            st.session_state.chat_history.append(
                {
                    "question": question,
                    "answer": answer,
                }
            )

        for chat in st.session_state.chat_history:

            with st.chat_message("user"):
                st.write(chat["question"])

            with st.chat_message("assistant"):
                st.write(chat["answer"])

    else:

        st.info(
            "📄 Upload a PDF and create the knowledge base first."
        )

# ======================================================
# Summary Tab
# ======================================================

with tab2:

    if st.session_state.db_created:

        st.header("📄 AI Summary")

        if st.button("Generate Summary"):

            with st.spinner("Generating Summary..."):

                summary = summarize_pdf()

            st.success("Summary Generated Successfully!")

            st.write(summary)

    else:

        st.info(
            "📄 Upload a PDF first."
        )

# ======================================================
# Quiz Tab
# ======================================================

with tab3:

    if st.session_state.db_created:

        st.header("📝 Quiz Generator")

        if st.button("Generate Quiz"):

            with st.spinner("Generating Quiz..."):

                quiz = generate_quiz()

            st.success("Quiz Generated Successfully!")

            st.write(quiz)

    else:

        st.info(
            "📄 Upload a PDF first."
        )

# ======================================================
# Flashcards Tab
# ======================================================

with tab4:

    if st.session_state.db_created:

        st.header("🗂 Flashcards")

        if st.button("Generate Flashcards"):

            with st.spinner("Generating Flashcards..."):

                flashcards = generate_flashcards()

            st.success("Flashcards Generated Successfully!")

            st.write(flashcards)

    else:

        st.info(
            "📄 Upload a PDF first."
        )

# ======================================================
# Footer
# ======================================================

st.divider()

