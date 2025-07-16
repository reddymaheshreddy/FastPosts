from fastapi import FastAPI, HTTPException, status, Response, Depends
from sqlalchemy.orm import Session
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from .routers import post, user,auth,votes

from . import models, schemas
from .database import engine, get_db
from .utils import hash

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
# CORS Middleware
app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def root():
    return {"message": "Hello FastAPI with SQLAlchemy and created_at"}


