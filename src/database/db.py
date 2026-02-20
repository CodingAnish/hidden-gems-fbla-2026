"""
Database Layer - SQLite Connection and Schema Management

Handles database connection pooling, table creation, and schema migrations.
All state is persisted in a local SQLite database for development.

Hidden Gems | FBLA 2026
"""
import os
import sqlite3
from pathlib import Path

# Database configuration
DATABASE_DIRECTORY = Path(__file__).resolve().parent.parent.parent  # Project root
DATABASE_PATH = DATABASE_DIRECTORY / "hidden_gems.db"


def get_connection():
    """
    Get a connection to the SQLite database.
    
    Configures row factory to allow accessing columns by name (like dictionaries).
    
    Returns:
        sqlite3.Connection: Database connection with row access by column name
    """
    connection = sqlite3.connect(DATABASE_PATH)
    # Allow accessing columns by name instead of index (Row objects act like dicts)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """
    Initialize database tables if they don't exist.
    
    Creates all required tables and performs schema migrations for backward compatibility.
    This function is idempotent - safe to call multiple times.
    """
    connection = get_connection()
    cursor = connection.cursor()

    # Create users table with email, password, verification, and profile info
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            email_verified INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """)
    
    # Schema migration: Add email verification status to existing databases
    cursor.execute("PRAGMA table_info(users)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    
    if "email_verified" not in existing_columns:
        # Add email_verified column and assume all existing users are verified
        cursor.execute("ALTER TABLE users ADD COLUMN email_verified INTEGER NOT NULL DEFAULT 1")
        connection.commit()
    
    # Schema migration: Add username field for user profiles
    if "username" not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN username TEXT")
        connection.commit()
        # Backfill usernames from email addresses (take part before @)
        cursor.execute("""
            UPDATE users 
            SET username = lower(
                replace(
                    replace(
                        substr(email, 1, instr(email || '@', '@') - 1), 
                    '.', '_'), 
                '+', '_')
            ) 
            WHERE username IS NULL
        """)
        connection.commit()
    
    # Schema migration: Add user preferences storage
    if "user_preferences" not in existing_columns:
        cursor.execute("ALTER TABLE users ADD COLUMN user_preferences TEXT")
        connection.commit()
    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username) WHERE username IS NOT NULL")

    # Email verification codes (sent to user / shown in demo)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS email_verification_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            code TEXT NOT NULL,
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Verification attempts - visible table for verification records
    cursor.execute("""
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
    cursor.execute("""
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
    cursor.execute("PRAGMA table_info(businesses)")
    business_columns = [row[1] for row in cursor.fetchall()]
    
    # Add missing columns if they don't exist
    if "address" not in business_columns:
        cursor.execute("ALTER TABLE businesses ADD COLUMN address TEXT")
        connection.commit()
    
    new_columns = {
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
    for col_name, col_type in new_columns.items():
        if col_name not in business_columns:
            cursor.execute(f"ALTER TABLE businesses ADD COLUMN {col_name} {col_type}")
            connection.commit()

    # Deals
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS deals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_id INTEGER NOT NULL,
            description TEXT NOT NULL,
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
    """)

    # Reviews - linked to user and business
    cursor.execute("""
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
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            business_id INTEGER NOT NULL,
            UNIQUE(user_id, business_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (business_id) REFERENCES businesses(id)
        )
    """)

    connection.commit()
    connection.close()
