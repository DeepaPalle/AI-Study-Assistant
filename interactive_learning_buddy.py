import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import PyPDF2
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="🤖",
    layout="wide"
)

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("models/gemini-2.5-flash")


st.markdown("""
<style>
    .gradient-header {
        background: linear-gradient(90deg, #3B82F6 0%, #8B5CF6 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .history-card {
        border: 1px solid #e5e7eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def get_response(prompt, difficulty="intermediate"):
    difficulty_prompts = {
        "beginner": "Explain this in simple terms for a beginner: ",
        "intermediate": "Provide a detailed explanation of: ",
        "advanced": "Give an in-depth technical analysis of: "
    }

    full_prompt = f"{difficulty_prompts[difficulty]}{prompt}"

    try:
        response = model.generate_content(full_prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None


def save_to_history(question, answer):
    if "history" not in st.session_state:
        st.session_state.history = []

    st.session_state.history.append({
        "question": question,
        "answer": answer
    })


def extract_text_from_pdf(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def split_text(text, chunk_size=700):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunks.append(" ".join(words[i:i + chunk_size]))

    return chunks


def get_relevant_chunks(question, chunks, top_k=3):
    if not chunks:
        return ""

    documents = chunks + [question]

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(vectors[-1], vectors[:-1]).flatten()
    top_indices = similarity.argsort()[-top_k:][::-1]

    return "\n\n".join([chunks[i] for i in top_indices])


def ask_pdf_question(question, chunks):
    context = get_relevant_chunks(question, chunks)

    prompt = f"""
You are an AI Study Assistant.

Answer the question using only the PDF content below.
If the answer is not present in the PDF, say:
"I could not find this information in the uploaded PDF."

PDF Content:
{context}

Question:
{question}

Give a clear student-friendly answer.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_quiz_from_pdf(chunks):
    context = "\n\n".join(chunks[:4])

    prompt = f"""
Based on the study material below, generate 5 multiple-choice questions.

Format:
Q1. Question
A. Option
B. Option
C. Option
D. Option
Answer: Correct option

Study Material:
{context}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_flashcards(chunks):
    context = "\n\n".join(chunks[:4])

    prompt = f"""
Create 10 flashcards from the study material below.

Format:
Flashcard 1
Q: question
A: answer

Study Material:
{context}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def summarize_notes(chunks):
    context = "\n\n".join(chunks[:4])

    prompt = f"""
Summarize the study material below in simple student-friendly language.

Include:
1. Short summary
2. Important points
3. Key terms

Study Material:
{context}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


with st.container():
    st.markdown(
        '<div class="gradient-header"><h1>🤖 AI Study Assistant</h1><p>Learn, generate quizzes, and ask questions from PDFs</p></div>',
        unsafe_allow_html=True
    )

    with st.sidebar:
        st.header("Settings")

        difficulty = st.select_slider(
            "Select difficulty level",
            options=["beginner", "intermediate", "advanced"],
            value="intermediate",
            key="difficulty_slider"
        )

        st.info("Upload a PDF in the PDF Q&A tab to generate answers, quizzes, summaries, and flashcards.")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📚 Learn",
        "🧩 Quiz",
        "📄 PDF Q&A",
        "📈 Review"
    ])

    with tab1:
        st.header("Learn Something New")

        user_prompt = st.text_area(
            "What would you like to learn about?",
            key="learn_prompt",
            height=100
        )

        if st.button("Get Answer", key="learn_button", use_container_width=True):
            if user_prompt:
                with st.spinner("Generating response..."):
                    response = get_response(user_prompt, difficulty)

                if response:
                    st.success("Here's your explanation:")
                    st.write(response)
                    save_to_history(user_prompt, response)
            else:
                st.warning("Please enter a question.")

    with tab2:
        st.header("Generate Quiz")

        quiz_topic = st.text_input(
            "Enter a topic for a quick quiz:",
            key="quiz_topic"
        )

        if st.button("Generate Quiz", key="quiz_button", use_container_width=True):
            if quiz_topic:
                with st.spinner("Creating your quiz..."):
                    quiz_prompt = f"""
Create a 5-question quiz about {quiz_topic} suitable for {difficulty} level.

For each question, provide:
A, B, C, D options and the correct answer.
"""
                    quiz = get_response(quiz_prompt, difficulty)

                if quiz:
                    st.success("Here's your quiz:")
                    st.write(quiz)
            else:
                st.warning("Please enter a topic for the quiz.")

    with tab3:
        st.header("PDF Study Tools")

        uploaded_pdf = st.file_uploader(
            "Upload your notes PDF",
            type=["pdf"]
        )

        if uploaded_pdf is not None:
            with st.spinner("Reading PDF..."):
                pdf_text = extract_text_from_pdf(uploaded_pdf)
                chunks = split_text(pdf_text)

            if len(chunks) == 0:
                st.error("No readable text found in this PDF.")
            else:
                st.success("PDF uploaded successfully!")

                st.subheader("Ask Questions from PDF")

                pdf_question = st.text_input(
                    "Ask a question from this PDF:",
                    key="pdf_question"
                )

                if st.button("Ask PDF", key="ask_pdf_button", use_container_width=True):
                    if pdf_question:
                        with st.spinner("Searching PDF and generating answer..."):
                            answer = ask_pdf_question(pdf_question, chunks)

                        st.write(answer)
                        save_to_history(pdf_question, answer)
                    else:
                        st.warning("Please enter a question.")

                st.divider()

                col1, col2, col3 = st.columns(3)

                with col1:
                    if st.button("Generate PDF Summary", use_container_width=True):
                        with st.spinner("Generating summary..."):
                            summary = summarize_notes(chunks)

                        st.subheader("PDF Summary")
                        st.write(summary)
                        save_to_history("PDF Summary", summary)

                with col2:
                    if st.button("Generate Quiz from PDF", use_container_width=True):
                        with st.spinner("Creating quiz..."):
                            quiz = generate_quiz_from_pdf(chunks)

                        st.subheader("Generated Quiz")
                        st.write(quiz)
                        save_to_history("PDF Quiz", quiz)

                with col3:
                    if st.button("Generate Flashcards", use_container_width=True):
                        with st.spinner("Creating flashcards..."):
                            cards = generate_flashcards(chunks)

                        st.subheader("Flashcards")
                        st.write(cards)
                        save_to_history("PDF Flashcards", cards)

    with tab4:
        st.header("Learning History")

        if "history" not in st.session_state or len(st.session_state.history) == 0:
            st.info("No history available yet. Start learning to see your previous topics here!")
        else:
            for i, item in enumerate(st.session_state.history):
                with st.expander(f"Topic {i + 1}", expanded=False):
                    st.markdown(f"""
                    <div class="history-card">
                        <h4>Question:</h4>
                        <p>{item['question']}</p>
                        <h4>Answer:</h4>
                        <p>{item['answer']}</p>
                    </div>
                    """, unsafe_allow_html=True)

        if st.button("Clear History", key="clear_history", use_container_width=True):
            st.session_state.history = []
            st.success("History cleared successfully!")