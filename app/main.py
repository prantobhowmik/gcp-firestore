from fastapi import FastAPI
from app.core.config import init_firestore
from app.api.v1.routes.files import router as files_router

app = FastAPI(title="GCP Firestore Learning")

# Initialize Firestore + Firebase Storage
init_firestore()

@app.get("/")
async def root():
    return {"message": "Welcome to learning GCP FIRESTORE!"}

app.include_router(files_router, prefix="/files", tags=["Files"])
