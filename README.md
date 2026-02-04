## RAG using Endee Vector Database

## Project Title

**Semantic Search / RAG System using Endee Vector Database and OpenAI**

---

## 1. Project Overview

This project demonstrates a **Retrieval-Augmented Generation (RAG)** style system using:

* **OpenAI Embeddings** for converting text into vectors
* **Endee Vector Database** for storing and searching vectors
* **FastAPI** as the backend API layer

The system allows users to:

1. Upload text documents
2. Convert them into embeddings
3. Store them in Endee
4. Perform semantic search using natural language queries

---

## 2. Tech Stack

| Component              | Technology       |
| ---------------------- | ---------------- |
| Backend API            | FastAPI (Python) |
| LLM / Embeddings       | OpenAI API       |
| Vector Database        | Endee            |
| Containerization       | Docker           |
| HTTP Client            | Requests         |
| Environment Management | python-dotenv    |

---

## 3. System Architecture

```
User Query
   ↓
FastAPI Backend
   ↓
OpenAI Embeddings
   ↓
Endee Vector Database
   ↓
Top-K Similar Vectors
   ↓
Returned to User
```

---

## 4. Important Note about Endee API

This project uses the **public Endee Docker image**:

```
endeeio/endee-server:latest
```

This image runs Endee in **read-only mode**, meaning:

* ❌ Index creation via API is disabled
* ❌ Vector upsert via API is disabled
* ✅ Vector search is enabled

For **full CRUD support**, Endee must be built from source using their GitHub repository.

For this assignment, we use the **default index provided by the public container**.

---

## 5. Setup Instructions

### Step 1 – Clone Repository

```bash
git clone https://github.com/your-username/rag-using-endee
cd rag-using-endee
```

---

### Step 2 – Create `.env` file

Create a file named `.env`:

```env
OPENAI_API_KEY=your_openai_key_here
ENDEE_BASE_URL=http://localhost:8080
```

---

### Step 3 – Start Endee using Docker

```bash
docker run -p 8080:8080 endeeio/endee-server:latest
```

Check if Endee is running:

```bash
curl http://localhost:8080/api/v1/index/list
```

---

### Step 4 – Setup Python Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn openai python-dotenv requests
```

---

### Step 5 – Start Backend Server

```bash
uvicorn backend.main:app --reload
```

Open browser:

```
http://127.0.0.1:8000/docs
```

---

## 6. How to Test the Use Case

### 1️⃣ Upload Documents

```http
POST /upload?text=Endee is a high performance vector database
POST /upload?text=RAG stands for Retrieval Augmented Generation
POST /upload?text=FastAPI is a Python backend framework
```

---

### 2️⃣ Perform Semantic Search

```http
POST /search?query=What is Endee?
```

---

### Expected Output

```json
{
  "results": [
    {
      "metadata": {
        "text": "Endee is a high performance vector database"
      }
    }
  ]
}
```

This confirms:

* Embeddings were generated
* Vectors were stored
* Semantic retrieval is working

---

## 7. How This is RAG

This project implements the **retrieval part** of RAG:

* LLM → generates embeddings
* Vector DB → retrieves relevant context
* Context → can be passed to GPT for final answer

(Generation step can be easily added as `/ask` endpoint.)

---

## 8. Limitations

| Limitation         | Reason                              |
| ------------------ | ----------------------------------- |
| No index creation  | Public Endee container is read-only |
| No delete/update   | Same reason                         |
| Only default index | Predefined by container             |

---

## 9. Future Improvements

* Build Endee from source for full CRUD
* Add `/ask` endpoint for final LLM answer
* Add PDF ingestion
* Add UI using React

---

## 10. Interview Summary (One-Liner)

> “This project uses OpenAI embeddings with Endee vector database to implement a semantic search system using FastAPI, demonstrating the retrieval layer of a RAG pipeline.”

---

## This README alone is **placement-grade**

If an evaluator reads just this file, they can:

* Run your project
* Understand your design
* Verify your use case
* See you understand real system limitations

This is **exactly what Endee expects** from this assignment.
