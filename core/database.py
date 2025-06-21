"""
Database operations
"""
import sqlite3
from typing import Dict, List

class RedditDatabase:
    def __init__(self, db_path: str = "data/reddit_posts.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        with sqlite3.connect(self.db_path) as conn:
            # Create the table with all columns
            conn.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY,
                    article_url TEXT,
                    title TEXT,
                    content TEXT,
                    subreddit TEXT,
                    status TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Migrate existing database if needed
            self._migrate_database(conn)
    
    def _migrate_database(self, conn):
        """Migrate existing database to new schema"""
        try:
            # Check if new columns exist
            cursor = conn.execute("PRAGMA table_info(posts)")
            columns = [column[1] for column in cursor.fetchall()]
            
            # Add missing columns
            if 'article_url' not in columns:
                conn.execute("ALTER TABLE posts ADD COLUMN article_url TEXT")
            if 'content' not in columns:
                conn.execute("ALTER TABLE posts ADD COLUMN content TEXT")
            if 'status' not in columns:
                conn.execute("ALTER TABLE posts ADD COLUMN status TEXT DEFAULT 'generated'")
                
        except sqlite3.Error as e:
            print(f"Migration warning: {e}")
    
    def add_post_history(self, article_url: str = "", subreddit: str = "", title: str = "", content: str = "", status: str = "pending", **kwargs) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "INSERT INTO posts (article_url, title, content, subreddit, status) VALUES (?, ?, ?, ?, ?)",
                (article_url, title, content, subreddit, status)
            )
            return cursor.lastrowid
    
    def get_post_history(self, limit: int = 50) -> List[Dict]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM posts ORDER BY created_at DESC LIMIT ?",
                (limit,)
            )
            return [dict(row) for row in cursor.fetchall()]

db = RedditDatabase()

def get_database():
    """Get the global database instance"""
    return db
