from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import os
import openai
import pandas as pd
from dotenv import load_dotenv
from .agent import nl_to_filter
from pinecone import Pinecone

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

class QueryRequest(BaseModel):
    question: str

class SearchResult(BaseModel):
    title: str
    author: str
    published_year: int
    published_month: int
    published_day: int
    tags: List[str]
    pageURL: str

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
INDEX_NAME = os.getenv("INDEX_NAME", "bridged-demo")

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index(INDEX_NAME)

@app.post("/query")
def query(request: QueryRequest):
    user_question = request.question
    try:
        pinecone_filter = nl_to_filter(user_question)

        if pinecone_filter == {}:
            return {
                "results": [],
                "message": "Your question is not relevant to our articles."
            }

        response = openai.Embedding.create(
            input=user_question,
            model="text-embedding-ada-002"
        )
        query_embedding = response['data'][0]['embedding']
        result = index.query(
            vector=query_embedding,
            filter=pinecone_filter,
            top_k=5,
            include_metadata=True
        )
        output = []
        for match in result['matches']:
            meta = match['metadata']
            output.append({
                "title": meta.get("title", ""),
                "author": meta.get("author", ""),
                "published_year": meta.get("published_year", ""),
                "published_month": meta.get("published_month", ""),
                "published_day": meta.get("published_day", ""),
                "tags": meta.get("tags", []),
                "pageURL": meta.get("pageURL", "")
            })

        if not output:
            return {
                "results": [],
                "message": "No matching articles found for your query."
            }

        return {"results": output}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
