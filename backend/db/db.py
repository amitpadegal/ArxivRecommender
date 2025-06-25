import chromadb
chroma_client = chromadb.Client()

# switch `create_collection` to `get_or_create_collection` to avoid creating a new collection every time
paper_collection = chroma_client.get_or_create_collection(name="papers")
user_collection = chroma_client.get_or_create_collection("users")

