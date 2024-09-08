import os
import json
import faiss
import numpy as np
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.schema import Document
from langchain.retrievers.merger_retriever import MergerRetriever
from langchain.text_splitter import RecursiveCharacterTextSplitter
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
    
def split_in_doc(text):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=20
    )
    chunks = text_splitter.split_text(text)


    # Convert chunks into Document objects
    documents = [Document(page_content=chunk) for chunk in chunks]
    return documents


# Function to create or load FAISS indexes for WordPress posts
def create_faiss_indexes(post_data):
    # Initialize the embedding model
    
    for index, post in enumerate(post_data):
        post_title = clean_title(post["title"]).replace(" ", "_")  # Create a safe filename
        index_path = os.path.join(INDEX_STORE_DIR, f"{post_title}")
        document = split_in_doc(post["content"])
        var_metadata = f"""
        This is a wordpress post which was posted by {post["user_name"]} on the topic {post["title"]}.
        You Can View this Post by clicking on the link given below.
        {post["short_url"]}
        This Post was posted on date {post["date"]} and last modified on {post["date_modified"]}.
        """
        
        if os.path.exists(index_path):
            print("Vector Stores already exist for this post")
        else:
            # Create a new index
            document.append(Document(page_content=var_metadata,
                              metadata={
                                "title": post["title"],
                                "short_url": post["short_url"],
                                "date":post["date"],
                                "date_modified":post["date_modified"]
                              }))
            vector_store = FAISS.from_documents(document, embeddings) 
            vector_store.save_local(index_path)
            print(f"Created new index for '{post['title']}'")


def merge_vector_stores(vector_store_root_dir=INDEX_STORE_DIR):
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