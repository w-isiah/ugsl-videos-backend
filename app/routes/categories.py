"""
Category API routes
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from app import queries

router = APIRouter(prefix="/categories", tags=["Categories"])


# ----------------------------
# SCHEMAS
# ----------------------------

class CategoryOut(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ""
    color: Optional[str] = ""


class CategoryUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    color: Optional[str] = None


class CategoryVideosOut(BaseModel):
    category: CategoryOut
    videos: List[dict]
    count: int


# ----------------------------
# ROUTES
# ----------------------------

@router.get("", response_model=dict)
def list_categories():
    """Get all categories"""
    categories = queries.get_categories()
    return {
        "success": True,
        "count": len(categories),
        "data": categories
    }


@router.get("/{category_id}", response_model=dict)
def get_category(category_id: int):
    """Get a single category by ID"""
    category = queries.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "data": category}


@router.post("", response_model=dict)
def create_category(data: CategoryCreate):
    """Create a new category"""
    category_id = queries.create_category(
        name=data.name,
        description=data.description,
        color=data.color
    )
    category = queries.get_category(category_id)
    return {"success": True, "data": category}


@router.put("/{category_id}", response_model=dict)
def update_category(category_id: int, data: CategoryUpdate):
    """Update an existing category"""
    success = queries.update_category(
        category_id,
        name=data.name,
        description=data.description,
        color=data.color
    )
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"success": True, "message": "Category updated"}


@router.delete("/{category_id}", response_model=dict)
def delete_category(category_id: int):
    """Delete a category (only if no videos are linked)"""
    success, message = queries.delete_category(category_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"success": True, "message": message}


@router.get("/{category_id}/videos", response_model=dict)
def list_category_videos(category_id: int):
    """Get all videos under a specific category"""
    category = queries.get_category(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    videos = queries.get_videos(category_id=category_id)
    return {
        "success": True,
        "category": category,
        "videos": videos,
        "count": len(videos)
    }
