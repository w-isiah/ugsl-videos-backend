from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
import os

from app.routes import videos, categories
from app.database import test_connection

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Ugandan Sign Language API",
    description="Backend API for Ugandan Sign Language Video Platform",
    version="1.0.0",
)

# ----------------------------
# Static files (LOCAL videos)
# ----------------------------
os.makedirs("videos", exist_ok=True)
app.mount("/videos", StaticFiles(directory="videos"), name="videos")

# ----------------------------
# CORS (allow your frontend)
# ----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite frontend
        "http://localhost:3000",  # optional CRA frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# Include Routers
# ----------------------------
# NOTE: The router already has prefix="/videos" inside videos.py
app.include_router(videos.router)      # do NOT add prefix here
app.include_router(categories.router, prefix="/categories", tags=["Categories"])

# ----------------------------
# Root & Health
# ----------------------------
@app.get("/")
def root():
    """Root endpoint"""
    return {"status": "OK", "message": "Ugandan Sign Language API", "docs": "/docs"}

@app.get("/health")
def health():
    """Check database connection"""
    return {
        "status": "healthy" if test_connection() else "unhealthy",
        "database": "connected" if test_connection() else "disconnected",
    }

# ----------------------------
# Run server (for direct execution)
# ----------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
