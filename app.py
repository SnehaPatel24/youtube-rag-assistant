import asyncio
from urllib.parse import urlparse, parse_qs


def get_video_id(url):
    """
    Extract YouTube video ID from different URL formats.
    """

    parsed = urlparse(url)

    # Short URL
    if parsed.hostname == "youtu.be":
        return parsed.path.lstrip("/")

    # Standard YouTube URLs
    if parsed.hostname in ("www.youtube.com", "youtube.com"):

        # https://www.youtube.com/watch?v=xxxx
        if parsed.path == "/watch":
            return parse_qs(parsed.query).get("v", [None])[0]

        # https://www.youtube.com/shorts/xxxx
        elif parsed.path.startswith("/shorts/"):
            return parsed.path.split("/")[2]

        # https://www.youtube.com/embed/xxxx
        elif parsed.path.startswith("/embed/"):
            return parsed.path.split("/")[2]

    return None


try:
    asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

import streamlit as st

from transcript import get_transcript
from rag import (
    split_transcript,
    create_vector_store,
    ask_question
)

st.set_page_config(
    page_title="YouTube RAG Assistant",
    page_icon="🎥",
    layout="wide"
)

st.title("🎥 YouTube Video Q&A Assistant")

st.write(
    "Ask questions about any YouTube video using AI-powered Retrieval-Augmented Generation (RAG)."
)

# -----------------------------
# Store Vector Store
# -----------------------------
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None


# -----------------------------
# YouTube URL
# -----------------------------
youtube_url = st.text_input(
    "Paste YouTube URL"
)


# -----------------------------
# Process Button
# -----------------------------
if st.button("Process Video"):

    if youtube_url == "":
        st.warning("Please enter a YouTube URL.")

    else:

        try:

            video_id = get_video_id(youtube_url)
            if video_id is None:
                st.error("❌ Invalid YouTube URL")
                st.stop()

            with st.spinner("Fetching transcript..."):

                transcript = get_transcript(video_id)

            if transcript is None:

                st.error("Transcript not available.")

            else:

                with st.spinner("Creating embeddings..."):

                    chunks = split_transcript(transcript)

                    vector_store = create_vector_store(chunks)

                    st.session_state.vector_store = vector_store

                st.success("Video processed successfully!")

        except Exception as e:
            import traceback
            st.error(str(e))
            st.code(traceback.format_exc())


st.divider()

# -----------------------------
# Question
# -----------------------------
question = st.text_input(
    "Ask a question"
)


if st.button("Ask"):

    if st.session_state.vector_store is None:

        st.warning("Please process a video first.")

    elif question == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Thinking..."):

            answer = ask_question(
                st.session_state.vector_store,
                question
            )

        st.subheader("Answer")

        st.write(answer)