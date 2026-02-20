#!/usr/bin/env python3
"""
Reset Database - Clear all users and related data
Run this to reset the database to a clean state.

Usage: python3 reset_database.py
"""
import sys
import os

# Setup path
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from src.database.db import get_connection

def reset_users():
    """Delete all users from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        # Get table list to check what exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        # Delete from tables if they exist
        tables_to_clear = ['reviews', 'favorites', 'email_verification_codes', 'user_preferences', 'users']
        
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
    success = reset_users()
    sys.exit(0 if success else 1)
