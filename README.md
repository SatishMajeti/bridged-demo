# bridged-demo

A Natural Language to Pinecone Query Agent

---

## Overview

This project is an AI-powered agent that converts natural language questions into Pinecone queries using vector search and metadata filtering.
It’s built with FastAPI, OpenAI, Pinecone, and pandas.

---

## Project Structure

```
bridged-demo/
├── app/
│   ├── main.py
│   ├── agent.py
│   ├── pinecone_utils.py
│   ├── preprocess_data.py
├── data/
│   ├── sample_data.xlsx
│   └── processed_data.csv
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── README.md
└── .env
```

---

## Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/bridged-demo.git
   cd bridged-demo
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # (Windows)
   # or
   source .venv/bin/activate  # (Mac/Linux)
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   * Copy `.env.example` to `.env` and fill in your API keys.
   * Example `.env`:

     ```
     OPENAI_API_KEY=your-openai-key
     PINECONE_API_KEY=your-pinecone-key
     PINECONE_ENV=your-pinecone-env
     INDEX_NAME=bridged-demo
     ```

5. **Preprocess the data:**

   ```bash
   python app/preprocess_data.py
   ```

6. **Index data to Pinecone:**

   ```bash
   python app/pinecone_utils.py
   ```

7. **Start the FastAPI app:**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## Using Docker

1. **Build the Docker image:**

   ```bash
   docker build -t bridged-demo-app .
   ```

2. **Run the container (default port 8000):**

   ```bash
   docker run --env-file .env -p 8000:8000 bridged-demo-app
   ```

3. **To run on a different port:**

   ```bash
   docker run --env-file .env -e PORT=9000 -p 9000:9000 bridged-demo-app
   ```

* The API will be available at [http://localhost:8000/docs](http://localhost:8000/docs) or your chosen port.

---

## API Usage

* **POST `/query`**

  * Body:

    ```json
    {
      "question": "Show me articles by Jane Doe from May 2025 about IPL2025."
    }
    ```
  * Response:

    ```json
    {
      "results": [
        {
          "title": "...",
          "author": "...",
          "published_year": 2025,
          "published_month": 5,
          "published_day": 1,
          "tags": ["..."],
          "pageURL": "..."
        }
      ]
    }
    ```

---

## Notes

* All data files (`data/sample_data.xlsx`, `data/processed_data.csv`) are included for test/demo purposes.
* The app uses the `PORT` environment variable for the API port (default is 8000).

---