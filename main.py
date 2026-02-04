from fastapi import FastAPI
from dotenv import load_dotenv
import os
import requests
from openai import OpenAI

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ENDEE_BASE_URL = os.getenv("ENDEE_BASE_URL")  # http://localhost:8080

client = OpenAI(api_key=OPENAI_API_KEY)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "RAG using Endee is running"}


# ------------------------
# CREATE INDEX (PUT)
# ------------------------
@app.post("/create_index")
def create_index():
    res = requests.put(
        f"{ENDEE_BASE_URL}/api/v1/index/create",
        params={
            "index_name": "documents",
            "dimension": 1536,
            "metric": "cosine"
        }
    )
    return res.text


# ------------------------
# UPSERT VECTOR (PUT)
# ------------------------
@app.post("/upload")
def upload_text(text: str):
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )

    vector = emb.data[0].embedding

    res = requests.put(
        f"{ENDEE_BASE_URL}/api/v1/vector/upsert",
        params={
            "index_name": "documents",
            "id": text[:20]
        },
        json={
            "vector": vector,
            "metadata": {"text": text}
        }
    )

    return {
        "status": "stored",
        "endee_response": res.text
    }


# ------------------------
# SEARCH (POST)
# ------------------------
@app.post("/search")
def search(query: str):
    emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=query
    )

    q_vector = emb.data[0].embedding

    res = requests.post(
        f"{ENDEE_BASE_URL}/api/v1/vector/search",
        params={
            "index_name": "documents",
            "top_k": 3
        },
        json={
            "vector": q_vector
        }
    )

    return res.json()
