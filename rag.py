from dotenv import load_dotenv

load_dotenv()

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import (
    GoogleGenerativeAIEmbeddings,
    ChatGoogleGenerativeAI,
)
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain


# ----------------------------
# Split Transcript
# ----------------------------
def split_transcript(transcript):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents([transcript])

    return chunks


# ----------------------------
# Create Vector Store
# ----------------------------
def create_vector_store(chunks):

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vector_store = FAISS.from_documents(
        chunks,
        embeddings
    )

    return vector_store


# ----------------------------
# Load Gemini LLM
# ----------------------------
def create_llm():

    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0
    )

    return llm


# ----------------------------
# Prompt
# ----------------------------
def create_prompt():

    prompt = ChatPromptTemplate.from_template(
        """
You are a helpful AI assistant.

Answer the user's question ONLY from the provided context.

If the answer is not available in the context, simply reply:

"I don't know based on the provided transcript."

Context:
{context}

Question:
{input}
"""
    )

    return prompt


# ----------------------------
# Retriever
# ----------------------------
def create_retriever(vector_store):

    retriever = vector_store.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever


# ----------------------------
# Create RAG Chain
# ----------------------------
def create_rag_chain(vector_store):

    llm = create_llm()

    prompt = create_prompt()

    retriever = create_retriever(vector_store)

    document_chain = create_stuff_documents_chain(
        llm,
        prompt
    )

    retrieval_chain = create_retrieval_chain(
        retriever,
        document_chain
    )

    return retrieval_chain


# ----------------------------
# Ask Question
# ----------------------------
def ask_question(vector_store, question):

    chain = create_rag_chain(vector_store)

    response = chain.invoke(
        {
            "input": question
        }
    )

    return response["answer"]