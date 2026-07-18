from transcript import get_transcript
from rag import split_transcript
from rag import create_vector_store
from rag import ask_question

url = input("Enter YouTube URL: ")

transcript = get_transcript(url)
chunks = split_transcript(transcript)

vector_store = create_vector_store(chunks)

while True:

    question = input("\nAsk a question (or type exit): ")

    if question.lower() == "exit":
        break

    answer = ask_question(vector_store, question)

    print("\nAnswer:")
    print(answer)