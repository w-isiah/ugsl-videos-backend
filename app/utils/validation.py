"""
Simple validation functions
"""
def validate_video(data):
    """Validate video data"""
    errors = []
    
    if not data.get('title'):
        errors.append("Title is required")
    
    if not data.get('video_url'):
        errors.append("Video URL is required")
    
    if not data.get('category_id'):
        errors.append("Category ID is required")
    
    return errors

def validate_category(data):
    """Validate category data"""
    errors = []
    
    if not data.get('name'):
        errors.append("Category name is required")
    
    return errors