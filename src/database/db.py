"""
Database layer - SQLite connection and schema.
Hidden Gems | FBLA 2026
"""
import os
import sqlite3
from pathlib import Path

# Database file path (next to project root, so it persists)
DB_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = DB_DIR / "hidden_gems.db"


def get_connection():
    """Return a connection to the local SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn


def init_db():
    """Create all tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    # Users table - email login + email verification
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email_verified INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    # Add email_verified to existing DBs that don't have it
    cur.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cur.fetchall()]
    if "email_verified" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 1")
        conn.commit()
    if "username" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN username TEXT")
        conn.commit()
        # Backfill: set username from email prefix for existing users
        cur.execute("UPDATE users SET username = lower(replace(replace(substr(email, 1, instr(email || '@', '@') - 1), '.', '_'), '+', '_')) WHERE username IS NULL")
        conn.commit()
    if "user_preferences" not in columns:
        cur.execute("ALTER TABLE users ADD COLUMN user_preferences TEXT")
        conn.commit()
    cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username) WHERE username IS NOT NULL")

    # Email verification codes (sent to user / shown in demo)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Verification attempts - visible table for verification records
    cur.execute("""
        CREATE TABLE IF NOT EXISTS verification_attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT,
            verification_type TEXT NOT NULL,
            question TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            user_answer TEXT,
            success INTEGER NOT NULL DEFAULT 0,
            attempted_at TEXT NOT NULL DEFAULT (datetime('now')),
            context TEXT NOT NULL
        )
    """)

    # Businesses - Enhanced with Yelp data and AI summary
    cur.execute("""
        CREATE TABLE IF NOT EXISTS businesses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            address TEXT,
            average_rating REAL NOT NULL DEFAULT 0,
            total_reviews INTEGER NOT NULL DEFAULT 0,
            phone TEXT,
            website TEXT,
            yelp_url TEXT,
            latitude REAL,
            longitude REAL,
            price_range TEXT,
            hours TEXT,
            photo_url TEXT,
            attributes TEXT,
            summary TEXT,
            yelp_id TEXT UNIQUE
        )
    """)
    cur.execute("PRAGMA table_info(businesses)")
    bcols = [row[1] for row in cur.fetchall()]
    
    # Add missing columns if they don't exist
    if "address" not in bcols:
        cur.execute("ALTER TABLE businesses ADD COLUMN address TEXT")
        conn.commit()
    
    new_cols = {
        "phone": "TEXT",
        "website": "TEXT",
        "yelp_url": "TEXT",
        "latitude": "REAL",
        "longitude": "REAL",
        "price_range": "TEXT",
        "hours": "TEXT",
        "photo_url": "TEXT",
        "attributes": "TEXT",
        "summary": "TEXT",
        "yelp_id": "TEXT"
    }
    for col_name, col_type in new_cols.items():
        if col_name not in bcols:
            cur.execute(f"ALTER TABLE businesses ADD COLUMN {col_name} {col_type}")
            conn.commit()

    # Deals
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
    """)

    # Reviews - linked to user and business
    cur.execute("""
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT NOT NULL,
            created_date TEXT NOT NULL,
            created_time TEXT NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Favorites - user bookmarks
    cur.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            UNIQUE(user_id, business_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
    """)

    conn.commit()
    conn.close()
