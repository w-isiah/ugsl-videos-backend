"""
Video API routes
"""
from fastapi import APIRouter, HTTPException, UploadFile, File, Query
from pydantic import BaseModel
from typing import Optional, List
from app import queries
import os
import shutil

router = APIRouter(prefix="/videos", tags=["Videos"])


# ----------------------------
# SCHEMAS
# ----------------------------

class VideoOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    video_url: str
    thumbnail_url: Optional[str]
    duration: Optional[int]
    difficulty: Optional[str]
    category_id: Optional[int]
    views: int
    likes: int
    created_at: str  # will store as ISO string


class VideoListResponse(BaseModel):
    count: int
    data: List[VideoOut]


class VideoCreate(BaseModel):
    title: str
    category_id: Optional[int] = None
    description: Optional[str] = ""
    difficulty: Optional[str] = "beginner"


# ----------------------------
# HELPERS
# ----------------------------

def serialize_video(video: dict) -> dict:
    """Convert datetime to ISO string"""
    video_copy = video.copy()
    if "created_at" in video_copy and hasattr(video_copy["created_at"], "isoformat"):
        video_copy["created_at"] = video_copy["created_at"].isoformat()
    return video_copy


# ----------------------------
# ROUTES
# ----------------------------

@router.get("", response_model=VideoListResponse)
def list_videos(
    limit: int = Query(50, ge=1, le=100),
    category_id: Optional[int] = None
):
    videos = queries.get_videos(limit, category_id)
    videos_serialized = [serialize_video(v) for v in videos]
    return {"count": len(videos_serialized), "data": videos_serialized}


@router.get("/{video_id}", response_model=VideoOut)
def get_single_video(video_id: int):
    video = queries.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return serialize_video(video)


@router.post("", response_model=VideoOut)
def create_video(data: VideoCreate):
    video_id = queries.create_video(
        title=data.title,
        video_url="",
        category_id=data.category_id,
        description=data.description,
        difficulty=data.difficulty,
    )
    video = queries.get_video(video_id)
    return serialize_video(video)


@router.post("/upload", response_model=dict)
async def upload_video(
    file: UploadFile = File(...),
    title: str = "Untitled",
    category_id: Optional[int] = None,
):
    os.makedirs("videos", exist_ok=True)

    file_path = os.path.join("videos", file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    video_url = f"/videos/{file.filename}"

    video_id = queries.create_video(
        title=title,
        video_url=video_url,
        category_id=category_id,
    )

    return {
        "success": True,
        "id": video_id,
        "video_url": video_url
    }


@router.post("/{video_id}/like")
def like_video(video_id: int):
    if not queries.like_video(video_id):
        raise HTTPException(status_code=404, detail="Video not found")
    return {"success": True}
