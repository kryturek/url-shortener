from fastapi import FastAPI, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, HttpUrl
from starlette.responses import RedirectResponse
import random
import string

from database import SessionLocal, URLModel

app = FastAPI(root_path="/")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class URLIn(BaseModel):
    original_url: HttpUrl

@app.get("/")
def home():
    return {'hello': 'world'}

@app.post("/shorten/")
def shorten_url(url_in: URLIn, request: Request, db: Session = Depends(get_db)):
    while True:
        short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        if not db.query(URLModel).filter(URLModel.short_code == short_code).first():
            break

    db_url = URLModel(short_code = short_code, original_url = str(url_in.original_url))
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    base_url = str(request.base_url)
    return {'shortened_url': f"{base_url}{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str, db: Session = Depends(get_db)):
    db_url = db.query(URLModel).filter(URLModel.short_code == short_code).first()
    if not db_url:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=db_url.original_url)