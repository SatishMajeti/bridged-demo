import os
import pandas as pd
from pinecone import Pinecone, ServerlessSpec
import openai
from dotenv import load_dotenv
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")
RESOURCE_CLOUD = os.getenv("RESOURCE_CLOUD", "aws")  # Default to AWS if not set
INDEX_NAME = os.getenv("INDEX_NAME", "bridged-demo")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def generate_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response['data'][0]['embedding']

def index_to_pinecone(data_path):
    df = pd.read_csv(data_path)

    pc = Pinecone(api_key=PINECONE_API_KEY)

    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=RESOURCE_CLOUD,            
                region=PINECONE_ENV     
            )
        )

    index = pc.Index(INDEX_NAME)

    for i, row in df.iterrows():
        vector = generate_embedding(row['title'])
        metadata = {
            "author": row['author'],
            "published_year": int(row['published_year']),
            "published_month": int(row['published_month']),
            "published_day": int(row['published_day']),
            "tags": eval(row['tags']) if isinstance(row['tags'], str) else row['tags'],
            "pageURL": row['pageURL'],
            "title": row['title']
        }
        index.upsert([
            (str(i), vector, metadata)
        ])
        print(f"Upserted {i+1}/{len(df)}")

    print("Indexing complete!")

if __name__ == "__main__":
    load_dotenv()
    data_path = os.path.join(os.path.dirname(__file__), "../data/processed_data.csv")
    index_to_pinecone(data_path)
