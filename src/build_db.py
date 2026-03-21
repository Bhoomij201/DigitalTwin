import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

# 📁 Define DB path
persist_directory = "db"

# Load memory
with open("data/processed/memory.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Total memory items:", len(data))

# 🚫 Optional: safety check (avoid empty DB)
if len(data) == 0:
    print("No data found ❌")
    exit()

# Convert into documents
docs = [
    Document(
        page_content=item["page_content"],
        metadata=item["metadata"]
    )
    for item in data
]

# Load embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# 🔥 IMPORTANT: delete old DB (avoid mixing old + new data)
import shutil
import os

if os.path.exists(persist_directory):
    shutil.rmtree(persist_directory)

# Create DB
db = Chroma.from_documents(
    docs,
    embedding,
    persist_directory=persist_directory
)

# Save DB
db.persist()

print("Saving DB at:", persist_directory)
print("Vector DB created ✅")