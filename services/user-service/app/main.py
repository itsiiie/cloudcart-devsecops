from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User
from .auth import hash_password
from pydantic import BaseModel

Base.metadata.create_all(bind=engine)

app = FastAPI(root_path="/api/users")


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def health():
    return {"status": "user service running"}

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "user created"}