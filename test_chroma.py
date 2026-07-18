from dotenv import load_dotenv
load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

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

vector_store = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    persist_directory="./chroma_db"
)

print("Vector Store Created Successfully!")
print("Number of Chunks:", len(documents))