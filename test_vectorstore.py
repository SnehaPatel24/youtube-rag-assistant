from transcript import get_transcript
from rag import split_transcript
from rag import create_vector_store

video_id = "U1ZAwSOI408"

transcript = get_transcript(video_id)

chunks = split_transcript(transcript)

vector_store = create_vector_store(chunks)

print("Vector Store Created Successfully!")