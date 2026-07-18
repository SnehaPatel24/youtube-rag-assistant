from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter

video_id = "dQw4w9WgXcQ"

transcript = YouTubeTranscriptApi().fetch(video_id)

# Convert transcript into one long string
text = " ".join(chunk.text for chunk in transcript)

print("Total characters:", len(text))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.create_documents([text])

print("Total Chunks:", len(chunks))

print("\nFirst Chunk:\n")
print(chunks[0].page_content)