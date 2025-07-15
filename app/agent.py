import os
import openai
import json
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

SCHEMA_DESCRIPTION = """
You are an expert assistant for Pinecone metadata filtering.
If the user's question related to cricket, IPL, or any known articles/topics in the dataset, respond with the data schema that is:
    - author: string
    - published_year: int
    - published_month: int
    - published_day: int
    - tags: list of string (e.g., ["Cricket", "IPL2025"])
    For list fields like tags, always use the $in operator for matching, e.g., "tags": {"$in": ["IPL2025"]}
    For tags, if the user mentions a name or phrase (e.g., "Rohit Sharma"), join the words and remove spaces to match the tag format in the data (e.g., "RohitSharma").
    Given a user's question, output ONLY a valid Python dictionary (no code, no explanations) representing the Pinecone filter.
    Do not include unnecessary fields; only those relevant to the query.

If the user's question is not related to cricket or IPL, respond with an empty dictionary {}.

"""


def nl_to_filter(user_query: str) -> dict:
    prompt = f"""{SCHEMA_DESCRIPTION}
User question: "{user_query}"
Pinecone metadata filter:"""
    
    response = openai.ChatCompletion.create(
        model="gpt-4.1-nano",
        messages=[
            {"role": "system", "content": SCHEMA_DESCRIPTION},
            {"role": "user", "content": f'User question: "{user_query}"\nPinecone metadata filter:'}
        ],
        temperature=0.0,
        max_tokens=256
    )
    
    answer = response['choices'][0]['message']['content'].strip()
    
    try:
        first_brace = answer.find('{')
        last_brace = answer.rfind('}')
        filter_dict = json.loads(answer[first_brace:last_brace+1].replace("'", '"'))
    except Exception as e:
        print("Could not parse filter dictionary:", answer)
        raise e

    return filter_dict

if __name__ == "__main__":
    test_queries = [
        "Show me articles by Jane Doe from May 2025 about IPL2025.",
        "Find all posts tagged 'MumbaiIndians' published in May.",
        "Anything about Rohit Sharma?",
        "Articles on Cricket in 2024.",
    ]

    for query in test_queries:
        print(f"\nUser Query: {query}")
        try:
            result = nl_to_filter(query)
            print("Pinecone Filter:", result)
        except Exception as e:
            print("Error:", e)
