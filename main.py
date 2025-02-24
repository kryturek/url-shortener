from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string

app = FastAPI()

url_mapping = {}

class URLIn(BaseModel):
    original_url: str

@app.get("/")
def home():
    return {"Hello": "World"}

@app.post("/shorten/")
def shorten_url(url_in: URLIn):
    short_code = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    url_mapping[short_code] = url_in.original_url
    return {'shortened_url': f"http://localhost:8000/{short_code}"}

@app.get("/{short_code}")
def redirect_url(short_code: str):
    if short_code not in url_mapping:
        raise HTTPException(status_code=404, detail="URL not found")
    return {"original_url": url_mapping[short_code]}