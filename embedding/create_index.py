import os
import json
import faiss
import numpy as np
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.retrievers.merger_retriever import MergerRetriever
 # Assuming this function is in a separate file

# Constants
INDEX_STORE_DIR = "doc_embedding_store"  # Directory for storing indexes
EMBEDDING_MODEL = "multi-qa-MiniLM-L6-cos-v1" 
DIMENSION = 384
embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

# Ensure the index storage directory exists
if not os.path.exists(INDEX_STORE_DIR):
    os.mkdir(INDEX_STORE_DIR)

def clean_title(title:str):

    if title.__contains__(":"):
        cleaned_title = "".join(title.split(":"))
        return cleaned_title
    else:
        return title


# Function to create or load FAISS indexes for WordPress posts
def create_faiss_indexes(post_data):
    # Initialize the embedding model
    
    for index, post in enumerate(post_data):
        post_title = clean_title(post["title"]).replace(" ", "_")  # Create a safe filename
        index_path = os.path.join(INDEX_STORE_DIR, f"{post_title}")
        
        if os.path.exists(index_path):
            print("Vector Stores already exist for this post")
        else:
            # Create a new index
            document = Document(
                page_content=post["content"],
                metadata={
                    "title": post["title"],
                    "short_url": post["short_url"]
                }
            )
            vector_store = FAISS.from_documents([document], embeddings) 
            vector_store.save_local(index_path)
            print(f"Created new index for '{post['title']}'")


def merge_vector_stores(vector_store_root_dir="vector_store_"):
    index_files = [f for f in os.listdir(vector_store_root_dir)]

    # Check the full path of each file
    full_paths = [os.path.join(vector_store_root_dir, f) for f in index_files]

    vec_S = []

    for vs in full_paths:
        vec_S.append(FAISS.load_local(vs,embeddings,allow_dangerous_deserialization=True))

    retrievers = [
        vector.as_retriever(
            search_type="similarity", 
            search_kwargs={"k": 4},
        )
        for vector in vec_S
    ]
    merged_retrievers = MergerRetriever(retrievers=retrievers)
    return merged_retrievers