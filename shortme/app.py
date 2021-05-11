from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from diskcache import Cache
from hashids import Hashids
import os


app = FastAPI(title="URL Shortner")

origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

storage = Cache("shme.db", eviction_policy="none")
hasher = Hashids(salt=os.getenv("SHORTME_SALT", "shortme"), min_length=5)
host = os.getenv("SHORTME_HOST", "http://localhost:8088")


class Status(BaseModel):
    message: str


class InUrl(BaseModel):
    target: str
    overwrite: Optional[str] = None


class OutUrl(BaseModel):
    short: str
    target: str
    overwrite: Optional[str] = None


def get_key():
    return hasher.encode(storage.incr("int_id"))


@app.post("/urls", response_model=OutUrl)
async def create_url(data: InUrl):
    key = data.overwrite or get_key()
    if storage.get(key):
        raise HTTPException(status_code=409, detail="Overwrite already exists")
    storage.set(key, data.target)
    return OutUrl(
        **{"short": f"{host}/{key}", "target": data.target, "overwrite": data.overwrite}
    )


@app.get("/{short}", response_class=RedirectResponse)
async def get_url(short: str):
    if target := storage.get(short):
        return RedirectResponse(target, status_code=301)
    else:
        raise HTTPException(status_code=404, detail="URL not found")
