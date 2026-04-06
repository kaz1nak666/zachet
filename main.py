from contextlib import asynccontextmanager
from fastapi import FastAPI
from db import init_db
from routers import books

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Library API", lifespan=lifespan)

app.include_router(books.router)

@app.get("/")
def read_root():
    return {"message": "Kaz1nakProject v2.0 - AUTO-DEPLOYED! 🚀✅"}

@app.get("/health")
def health_check():
    return {"status": "ok", "deployed_by": "GitHub Actions + Self-Hosted Runner"}