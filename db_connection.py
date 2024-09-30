import pymongo
from pymongo import MongoClient
import json

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['NewsDB']
collection = db['articles']

# Function to insert data from JSON file into MongoDB
def insert_data(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        articles_data = json.load(f)

    result = collection.insert_many(articles_data)
    print(f"Inserted {len(result.inserted_ids)} articles into the MongoDB collection.")

if __name__ == "__main__":
    json_file = 'scraped_articles.json'
    insert_data(json_file)
