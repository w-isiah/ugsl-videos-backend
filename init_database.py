"""
Initialize database with sample data
"""
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def init_database():
    """Create database and tables"""
    
    # Connect without database first
    connection = pymysql.connect(
        host=os.getenv('DB_HOST', 'localhost'),
        user=os.getenv('DB_USER', 'root'),
        password=os.getenv('DB_PASSWORD', '')
    )
    
    try:
        with connection.cursor() as cursor:
            # Create database
            db_name = os.getenv('DB_NAME', 'ugsl_db')
            print(f"Creating database: {db_name}")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
            cursor.execute(f"USE {db_name}")
            
            print("Creating tables...")
            # Create categories table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS categories (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    description TEXT,
                    icon VARCHAR(50),
                    color VARCHAR(20) DEFAULT '#2196F3'
                )
            """)
            print("✅ Created categories table")
            
            # Create videos table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS videos (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    title VARCHAR(200) NOT NULL,
                    description TEXT,
                    video_url VARCHAR(500) NOT NULL,
                    thumbnail_url VARCHAR(500),
                    duration INT,
                    difficulty ENUM('beginner', 'intermediate', 'advanced') DEFAULT 'beginner',
                    category_id INT,
                    views INT DEFAULT 0,
                    likes INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
                )
            """)
            print("✅ Created videos table")
            
            # Check if categories table is empty
            cursor.execute("SELECT COUNT(*) as count FROM categories")
            result = cursor.fetchone()
            category_count = result[0]  # Access tuple by index, not key
            
            print(f"Found {category_count} existing categories")
            
            if category_count == 0:
                print("Inserting sample categories...")
                categories = [
                    ("Basic Communication", "Everyday greetings and expressions", "chat", "#2196F3"),
                    ("Educational Signs", "Academic and classroom vocabulary", "school", "#4CAF50"),
                    ("Health & Emergency", "Medical terms and emergency communication", "medical_services", "#F44336"),
                    ("Professional Contexts", "Workplace and business terminology", "business", "#FF9800"),
                    ("Cultural References", "Ugandan cultural signs and idioms", "language", "#9C27B0"),
                    ("Children's Learning", "Age-appropriate signs for young learners", "child_care", "#00BCD4")
                ]
                
                for cat in categories:
                    cursor.execute(
                        "INSERT INTO categories (name, description, icon, color) VALUES (%s, %s, %s, %s)",
                        cat
                    )
                print(f"✅ Inserted {len(categories)} categories")
                
                # Check if videos table is empty
                cursor.execute("SELECT COUNT(*) FROM videos")
                video_count = cursor.fetchone()[0]
                
                if video_count == 0:
                    print("Inserting sample videos...")
                    videos = [
                        ("Greetings & Introductions", "Learn basic greetings in Ugandan Sign Language", "/videos/greetings.mp4", 1, "beginner"),
                        ("Family Members", "Signs for family relationships", "/videos/family.mp4", 1, "beginner"),
                        ("Classroom Vocabulary", "Common signs used in educational settings", "/videos/classroom.mp4", 2, "beginner"),
                        ("Medical Emergency", "Emergency medical communication signs", "/videos/medical.mp4", 3, "intermediate")
                    ]
                    
                    for video in videos:
                        cursor.execute(
                            "INSERT INTO videos (title, description, video_url, category_id, difficulty) VALUES (%s, %s, %s, %s, %s)",
                            video
                        )
                    print(f"✅ Inserted {len(videos)} sample videos")
            
            connection.commit()
            print("\n✅ Database initialized successfully!")
            print(f"Database: {db_name}")
            print(f"Host: {os.getenv('DB_HOST', 'localhost')}")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    print("=" * 50)
    print("Ugandan Sign Language Database Initialization")
    print("=" * 50)
    init_database()