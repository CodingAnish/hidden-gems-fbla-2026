#!/usr/bin/env python3
"""
Database Reset Script - Clear all users and related data

Usage: python3 reset_db.py

This script clears all users, verification codes, favorites, reviews, and preferences.
Safe to run at any time - useful for testing or resetting the database.
"""
import sys
import os

# Setup path
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database.db import get_connection

def reset_database():
    """Clear all user data from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Tables to clear (in order of dependencies)
        tables_to_clear = [
            'reviews', 
            'favorites', 
            'email_verification_codes', 
            'user_preferences', 
            'users'
        ]
        
        # Clear each table if it exists
        for table in tables_to_clear:
            if table in tables:
                cursor.execute(f"DELETE FROM {table}")
                deleted = cursor.rowcount
                if deleted > 0:
                    print(f"✓ Cleared {deleted} rows from {table}")
        
        conn.commit()
        print("\n✓ Database reset successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Error resetting database: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    success = reset_database()
    sys.exit(0 if success else 1)
