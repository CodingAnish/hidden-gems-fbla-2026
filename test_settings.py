#!/usr/bin/env python3
"""Test settings page functionality"""
import sys
import os
import sqlite3

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# Get a test user from database
db_path = os.path.join(ROOT, 'hidden_gems.db')
conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

print("=" * 60)
print("CHECKING DATABASE FOR TEST USER")
print("=" * 60)

cur.execute("SELECT id, email, username, email_verified FROM users LIMIT 5")
users = cur.fetchall()
conn.close()

if not users:
    print("✗ No users found in database!")
    sys.exit(1)

print(f"\nFound {len(users)} users:\n")
for i, u in enumerate(users, 1):
    print(f"{i}. Email: {u['email']}, Username: {u['username']}, Verified: {u['email_verified']}")

print("\n" + "=" * 60)
print("TESTING SETTINGS PAGE")
print("=" * 60)

# Use first verified user, or any user if none verified
test_user = None
for u in users:
    if u['email_verified']:
        test_user = u
        print(f"\n✓ Using verified user: {u['email']}")
        break

if not test_user:
    test_user = users[0]
    print(f"\n⚠ No verified users, using: {test_user['email']}")

print("\nTo test the settings page:")
print(f"1. Login at http://localhost:5001/login")
print(f"   - Email/Username: {test_user['email']}")
print(f"   - Password: (you set this during registration)")
print(f"2. Go to http://localhost:5001/settings")
print(f"3. Verify:")
print(f"   - Account Settings heading appears")
print(f"   - Login/Sign Up buttons DO NOT appear")
print(f"   - Preferences form is present")
print(f"   - Save buttons work and data persists")
