from dotenv import load_dotenv
import os

load_dotenv()

key = os.getenv("GOOGLE_API_KEY")

print("Key:", key)
print("Starts with:", key[:10])
print("Length:", len(key))