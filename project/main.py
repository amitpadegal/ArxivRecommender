from fastapi import FastAPI
from fetch import fetch_arxiv_papers
from db.db_methods import insert_papers, get_papers

app = FastAPI()

@app.get("/")
async def fetch(query:str):
    papers = fetch_arxiv_papers("cs.CL", max_results=5)
    documents = [paper["summary"] for paper in papers]
    ids = [paper["url"] for paper in papers]
    metadatas = [{"title": paper["title"], "authors": ", ".join(paper["authors"]), "published": paper["published"]} for paper in papers]
    insert_papers("arxiv_papers", documents, ids, metadatas)
    out = get_papers("arxiv_papers", query, limit=1)
    print(f"Retrieved {len(out[0])} papers from the database.")
    return out
