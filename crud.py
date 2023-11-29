from sqlalchemy.orm import Session
from models import Repository
from sqlalchemy import select

def get_repository_from_db(db: Session, full_name: str):
    stmt = select(Repository).where(Repository.full_name == full_name)
    result = db.execute(stmt)
    return result.scalars().first()

def add_repository_to_db(db: Session, repo_data):
    db_repo = Repository(**repo_data)
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo
