import httpx
import time
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from models import SessionLocal, engine, Base
from crud import add_repository_to_db, get_repository_from_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/repositories/{owner}/{repository_name}")
def get_repository(owner: str, repository_name: str, db: Session = Depends(get_db)):
    url = f"https://api.github.com/repos/{owner}/{repository_name}"
    full_name = f"{owner}/{repository_name}"
    
    # Check if repository is in the database
    db_repo = get_repository_from_db(db, full_name)
    if db_repo:
        print('Returning data cached from db')
        return db_repo
    
    # api call if repo not cached in db
    with httpx.Client() as client:
        response = client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Repository not found")

        data = response.json()
        response_data = {
            "full_name": data["full_name"], 
            "description": data["description"],
            "clone_url": data["clone_url"],
            "stars": data["stargazers_count"],
            "created_at": data["created_at"]
        }
        add_repository_to_db(db, response_data)
        print('Repo added to db')
        return response_data
