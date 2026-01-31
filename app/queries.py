"""
SQL Query Layer - Handles all database interactions
"""
from typing import Optional, List, Dict, Tuple
from app.database import get_cursor


# ----------------------------
# VIDEOS
# ----------------------------

def get_videos(limit: int = 50, category_id: Optional[int] = None) -> List[Dict]:
    """Fetch videos, optionally filtered by category, newest first"""
    query = "SELECT * FROM videos"
    params: List = []

    if category_id is not None:
        query += " WHERE category_id = %s"
        params.append(category_id)

    query += " ORDER BY created_at DESC LIMIT %s"
    params.append(limit)

    with get_cursor() as cursor:
        cursor.execute(query, params)
        return cursor.fetchall()


def get_video(video_id: int) -> Optional[Dict]:
    """Fetch a single video and increment its view count"""
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM videos WHERE id = %s", (video_id,))
        video = cursor.fetchone()
        if video:
            cursor.execute("UPDATE videos SET views = views + 1 WHERE id = %s", (video_id,))
        return video


def create_video(
    title: str,
    video_url: str,
    category_id: Optional[int] = None,
    description: str = "",
    difficulty: str = "beginner"
) -> int:
    """Insert a new video and return its ID"""
    with get_cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO videos (title, video_url, category_id, description, difficulty)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, video_url, category_id, description, difficulty)
        )
        return cursor.lastrowid


def like_video(video_id: int) -> bool:
    """Increment like count for a video"""
    with get_cursor() as cursor:
        cursor.execute("UPDATE videos SET likes = likes + 1 WHERE id = %s", (video_id,))
        return cursor.rowcount > 0


def search_videos(search_term: str, limit: int = 20) -> List[Dict]:
    """Search videos by title or description"""
    with get_cursor() as cursor:
        cursor.execute(
            """
            SELECT * FROM videos
            WHERE title LIKE %s OR description LIKE %s
            ORDER BY created_at DESC
            LIMIT %s
            """,
            (f"%{search_term}%", f"%{search_term}%", limit)
        )
        return cursor.fetchall()


# ----------------------------
# CATEGORIES
# ----------------------------

def get_categories() -> List[Dict]:
    """Fetch all categories sorted by name"""
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM categories ORDER BY name")
        return cursor.fetchall()


def get_category(category_id: int) -> Optional[Dict]:
    """Fetch a single category by ID"""
    with get_cursor() as cursor:
        cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
        return cursor.fetchone()


def create_category(name: str, description: str = "", color: str = "") -> int:
    """Insert a new category and return its ID"""
    with get_cursor() as cursor:
        cursor.execute(
            "INSERT INTO categories (name, description, color) VALUES (%s, %s, %s)",
            (name, description, color)
        )
        return cursor.lastrowid


def update_category(
    category_id: int,
    name: str,
    description: Optional[str] = None,
    color: Optional[str] = None
) -> bool:
    """Update an existing category"""
    with get_cursor() as cursor:
        cursor.execute(
            "UPDATE categories SET name=%s, description=%s, color=%s WHERE id=%s",
            (name, description, color, category_id)
        )
        return cursor.rowcount > 0


def delete_category(category_id: int) -> Tuple[bool, str]:
    """
    Delete a category if no videos are linked.
    Returns (success, message)
    """
    with get_cursor() as cursor:
        cursor.execute("SELECT COUNT(*) AS count FROM videos WHERE category_id = %s", (category_id,))
        if cursor.fetchone()["count"] > 0:
            return False, "Cannot delete: This category still has videos."

        cursor.execute("DELETE FROM categories WHERE id = %s", (category_id,))
        return True, "Category deleted successfully"
