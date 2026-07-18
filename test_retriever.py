from dotenv import load_dotenv
load_dotenv()

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

# Get transcript
transcript = YouTubeTranscriptApi().fetch("dQw4w9WgXcQ")
text = " ".join(chunk.text for chunk in transcript)

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs = splitter.create_documents([text])

# Embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001"
)

# Create Vector Store
vectorstore = Chroma.from_documents(
    docs,
    embeddings
)

# Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

query = "What is this song about?"

results = retriever.invoke(query)

for i, doc in enumerate(results):
    print(f"\nChunk {i+1}\n")
    print(doc.page_content)