from fastapi import FastAPI, Request, HTTPException
from fetch import fetch_arxiv_papers
from db.db_methods import insert_papers, get_papers, get_or_initialize_user_vector, check_papers_exist, return_papers, update_user_vector_with_feedback
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin_init import verify_token_and_get_uid

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def fetch(query:str):
    papers = fetch_arxiv_papers("cs.CL", max_results=5)
    documents = [paper["summary"] for paper in papers]
    ids = [paper["url"] for paper in papers]
    metadatas = [{"title": paper["title"], "authors": ", ".join(paper["authors"]), "published": paper["published"]} for paper in papers]
    insert_papers(documents, ids, metadatas)
    out = get_papers(query, limit=1)
    print(f"Retrieved {len(out[0])} papers from the database.")
    return out

@app.get("/recommend")
async def recommend(request: Request):
    print("🔥 Backend received /recommend request")
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split("Bearer ")[1]
    try:
        uid = verify_token_and_get_uid(token)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")

    user_vector = get_or_initialize_user_vector(uid)
    print("before")
    # Check if any papers are present
    if not check_papers_exist():
        print("No papers found, fetching from arXiv...")
        papers = fetch_arxiv_papers("cs.CL", max_results=150)
        documents = [paper["summary"] for paper in papers]
        ids = [paper["url"] for paper in papers]
        print(ids)
        metadatas = [{"title": paper["title"], "authors": ", ".join(paper["authors"]), "published": paper["published"]} for paper in papers]
        insert_papers(documents, ids, metadatas)

    print("after")
    result = return_papers(user_vector)
    print(result)

    return {
        "uid": uid,
        "papers": result
    }

@app.post("/feedback")
async def receive_feedback(request: Request):
    print("🔥 Backend received /feedback request")
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing token")

    token = auth_header.split("Bearer ")[1]
    try:
        uid = verify_token_and_get_uid(token)
    except Exception as e:
        raise HTTPException(status_code=403, detail=f"Invalid token: {str(e)}")

    body = await request.json()
    feedback = body.get("feedback", {})  # {paper_id: 1 or -1, ...}

    # ⏬ Get current user vector
    user_vector = get_or_initialize_user_vector(uid)

    # ⬆️ Update it based on feedback
    update_user_vector_with_feedback(user_vector, feedback, uid)

    return {"status": "success"}

