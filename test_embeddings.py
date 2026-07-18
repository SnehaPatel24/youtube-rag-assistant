from dotenv import load_dotenv
load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

video_id = "dQw4w9WgXcQ"

transcript = YouTubeTranscriptApi().fetch(video_id)

text = " ".join(chunk.text for chunk in transcript)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

documents = splitter.create_documents([text])

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

vector = embeddings.embed_query(documents[0].page_content)

print("Embedding dimension:", len(vector))
print(vector[:10])