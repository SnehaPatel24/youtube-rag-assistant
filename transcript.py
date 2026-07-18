from youtube_transcript_api import YouTubeTranscriptApi
import streamlit as st


def get_transcript(video_id):
    try:
        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        return " ".join(item.text for item in transcript)

    except Exception as e:
        st.exception(e)
        raise