import chromadb
from db.db import chroma_client

# switch `add` to `upsert` to avoid adding the same documents every time
def insert_papers(collection_name, documents, ids=None, metadatas=None):
    """
    Inserts documents into the Chroma DB collection with optional metadata.

    Args:
        collection_name (str): Name of the collection.
        documents (list): List of documents to insert.
        ids (list, optional): List of unique IDs for the documents. Defaults to None.
        metadatas (list, optional): List of metadata dictionaries for the documents. Defaults to None.
    """
    collection = chroma_client.get_or_create_collection(name=collection_name)
    
    # Upsert documents into the collection with metadata
    collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas,
    )
    print(f"Inserted {len(documents)} documents into collection '{collection_name}'.")

def get_papers(collection_name, query, limit=10):
    """
    Retrieves documents and their metadata from the Chroma DB collection.

    Args:
        collection_name (str): Name of the collection.
        limit (int): Maximum number of documents to retrieve. Defaults to 10.

    Returns:
        tuple: A tuple containing a list of documents and their metadata.
    """
    collection = chroma_client.get_collection(name=collection_name)
    
    # Retrieve documents from the collection
    # results = collection.get(limit=limit)
    results = collection.query(
    query_texts=query,
    n_results=limit,
)
    return results['documents'], results['ids'], results.get('metadatas', [])