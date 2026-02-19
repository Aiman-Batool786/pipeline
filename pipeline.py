import pandas as pd
import json
from scraper import get_product_info
from openai_client import improve_product_content
from category_utils import assign_category
from Db import create_table, insert_product

def run_pipeline():
    create_table()

    df = pd.read_csv("products.csv")

    # Fix column names (lowercase, strip spaces)
    df.columns = df.columns.str.strip().str.lower()

    # If CSV column is 'urls', rename to 'url'
    if "urls" in df.columns:
        df.rename(columns={"urls": "url"}, inplace=True)

    for index, row in df.iterrows():
        url = row["url"]
        print("Processing:", url)

        data = get_product_info(url)
        if not data:
            print("Skipping URL due to scraping failure:", url)
            continue

        title = data["title"]
        description = data["description"]

        improved = improve_product_content(title, description)
        if not improved:
            print("Skipping URL due to OpenAI failure:", url)
            continue

        category = assign_category(improved["title"], improved["description"])

        insert_product((
            url,
            title,
            description,
            improved["title"],
            improved["description"],
            json.dumps(improved["bullet_points"]),
            category["category_id"],
            category["category_name"],
            category["confidence"]
        ))

        print("Saved successfully:", url)

if __name__ == "__main__":
    run_pipeline()
