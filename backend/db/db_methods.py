import chromadb
from db.db import paper_collection, user_collection
import numpy as np
import random

VECTOR_DIM = 768  # or 512 etc. depending on your embedding model

# switch `add` to `upsert` to avoid adding the same documents every time
def insert_papers(documents, ids=None, metadatas=None):
    """
    Inserts documents into the Chroma DB collection with optional metadata.

    Args:
        collection_name (str): Name of the collection.
        documents (list): List of documents to insert.
        ids (list, optional): List of unique IDs for the documents. Defaults to None.
        metadatas (list, optional): List of metadata dictionaries for the documents. Defaults to None.
    """
    # collection = chroma_client.get_or_create_collection(name=collection_name)
    
    # Upsert documents into the collection with metadata
    paper_collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas,
    )

def get_papers(query, limit=10):
    """
    Retrieves documents and their metadata from the Chroma DB collection.

    Args:
        collection_name (str): Name of the collection.
        limit (int): Maximum number of documents to retrieve. Defaults to 10.

    Returns:
        tuple: A tuple containing a list of documents and their metadata.
    """
    
    # Retrieve documents from the collection
    # results = collection.get(limit=limit)
    results = paper_collection.query(
    query_texts=query,
    n_results=limit,
)
    return results['documents'], results['ids'], results.get('metadatas', [])



def get_or_initialize_user_vector(uid: str):
    try:
        result = user_collection.get(ids=[uid], include=["embeddings"])
        return result["embeddings"][0]
    except Exception:
        # User not found — bootstrap with zero vector
        empty_vector = np.zeros(VECTOR_DIM).tolist()
        user_collection.upsert(
            ids=[uid],
            embeddings=[empty_vector],
            metadatas=[{"status": "new"}]
        )
        return empty_vector

def search_similar_papers(user_vector, top_k=5):
    results = paper_collection.query(
        query_embeddings=[user_vector],
        n_results=top_k,
        where={"type": "paper"},
        include=["documents", "metadatas"]
    )
    return results

def get_random_papers(count=5):
    all_papers = paper_collection.get(
        include=["documents", "metadatas"]
    )
    if not all_papers["documents"]:
        return []
    
    indices = random.sample(range(len(all_papers["documents"])), min(count, len(all_papers["documents"])))
    return {
        "documents": [all_papers["documents"][i] for i in indices],
        "metadatas": [all_papers["metadatas"][i] for i in indices],
    }

def return_papers(user_vector, top_k=5):
    """
    Returns papers based on the user vector.
    
    Args:
        user_vector (list): The user's vector representation.
        top_k (int): Number of top similar papers to return.
    
    Returns:
        dict: A dictionary containing the documents and their metadata.
    """
    if all(v == 0.0 for v in user_vector):
        return get_random_papers(count=top_k)
    else:
        return search_similar_papers(user_vector, top_k)

def check_papers_exist():
    """
    Checks if any papers exist in the collection.
    
    Returns:
        bool: True if papers exist, False otherwise.
    """
    all_papers = paper_collection.get()
    return len(all_papers["ids"]) > 0