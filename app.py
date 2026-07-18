import asyncio
import streamlit as st

# -------------------------------------------------
# Fix asyncio event loop issue in Streamlit
# -------------------------------------------------
try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

from transcript import get_transcript
from rag import (
    split_transcript,
    create_vector_store,
    ask_question,
)

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------
st.set_page_config(
    page_title="YouTube Video Q&A Assistant",
    page_icon="🎥",
    layout="centered",
)

# -------------------------------------------------
# Session State
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("🎥 YouTube Video Q&A Assistant")

st.caption(
    "Ask questions about any YouTube video using **Google Gemini + Retrieval-Augmented Generation (RAG)**."
)

st.divider()

# -------------------------------------------------
# Sidebar
# -------------------------------------------------
with st.sidebar:

    st.header("📌 About")

    st.write("""
This application can:

- 📺 Extract YouTube transcripts
- ✂️ Split transcripts into chunks
- 🧠 Create embeddings
- 📚 Store vectors using FAISS
- 🤖 Answer questions using Gemini
""")

    st.divider()

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.success("Chat cleared!")

    st.divider()

    st.success("Ready")

# -------------------------------------------------
# YouTube URL
# -------------------------------------------------
youtube_url = st.text_input(
    "Paste YouTube URL",
    placeholder="https://www.youtube.com/watch?v=..."
)

# -------------------------------------------------
# Process Video
# -------------------------------------------------
if st.button("🚀 Process Video"):

    if youtube_url.strip() == "":
        st.warning("Please enter a YouTube URL.")

    else:

        try:

            # Handle both URL formats
            if "youtu.be/" in youtube_url:
                video_id = youtube_url.split("youtu.be/")[1].split("?")[0]

            elif "v=" in youtube_url:
                video_id = youtube_url.split("v=")[1].split("&")[0]

            else:
                st.error("Invalid YouTube URL.")
                st.stop()

            with st.spinner("Fetching transcript..."):

                transcript = get_transcript(video_id)

            if transcript is None:
                st.error("Transcript not available.")
                st.stop()

            with st.spinner("Creating knowledge base..."):

                chunks = split_transcript(transcript)

                vector_store = create_vector_store(chunks)

            st.session_state.vector_store = vector_store

            # Start a fresh conversation for every new video
            st.session_state.messages = []

            st.success("✅ Video processed successfully!")

        except Exception as e:
            st.exception(e)

# -------------------------------------------------
# Chat History
# -------------------------------------------------
st.divider()

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# Ask Question
# -------------------------------------------------
question = st.chat_input("Ask a question about this video...")

if question:

    if st.session_state.vector_store is None:

        st.warning("Please process a YouTube video first.")

    else:

        # Show user message immediately
        st.session_state.messages.append(
            {
                "role": "user",
                "content": question
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):

            with st.spinner("Thinking..."):

                answer = ask_question(
                    st.session_state.vector_store,
                    question
                )

            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer
            }
        )

        st.rerun()