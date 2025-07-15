import pandas as pd
from datetime import datetime
import ast
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data/sample_data.xlsx")

def clean_tags(tag_str):
    """
    Converts tag string (e.g., '["#IPL2025", "#MumbaiIndians"]')
    into a Python list of strings without the '#' symbol.
    """
    try:
        tag_list = ast.literal_eval(tag_str)
        return [t.lstrip('#').strip() for t in tag_list]
    except Exception:
        return []

def preprocess():
    df = pd.read_excel(DATA_PATH)

    df['publishedDate'] = pd.to_datetime(df['publishedDate'])
    df['published_year'] = df['publishedDate'].dt.year
    df['published_month'] = df['publishedDate'].dt.month
    df['published_day'] = df['publishedDate'].dt.day
    df['tags'] = df['tags'].apply(clean_tags)

    pinecone_data = df[[
        'title',
        'author',
        'published_year',
        'published_month',
        'published_day',
        'tags',
        'pageURL'
    ]]

    return pinecone_data

if __name__ == "__main__":
    processed = preprocess()
    print(processed.head())

    output_dir = os.path.join(os.path.dirname(__file__), "../data")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, "processed_data.csv")
    processed.to_csv(output_path, index=False)
