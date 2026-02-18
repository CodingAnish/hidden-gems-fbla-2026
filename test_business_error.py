#!/usr/bin/env python3
"""Test business detail route to find the 500 error"""
import sys
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

os.chdir(ROOT)

from src.database import queries
from src.database.db import get_connection

print("=" * 70)
print("FINDING BUSINESS DETAIL ERROR")
print("=" * 70)

# Get a test user
conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT id, email FROM users WHERE email_verified = 1 LIMIT 1")
user_data = cur.fetchone()
conn.close()

if not user_data:
    print("✗ No verified users found")
    sys.exit(1)

user_id, user_email = user_data
print(f"\n✓ Using test user: {user_email} (ID: {user_id})")

# Check if businesses exist
print(f"\n1. CHECKING BUSINESSES IN DATABASE")
print("-" * 70)

businesses = queries.get_all_businesses()
if not businesses:
    print("✗ No businesses in database!")
    sys.exit(1)

print(f"✓ Found {len(businesses)} businesses")
first_biz = businesses[0]
print(f"  First business ID: {first_biz.get('id')}")
print(f"  Name: {first_biz.get('name')}")

# Try to get that business by ID directly
print(f"\n2. GETTING BUSINESS BY ID")
print("-" * 70)

biz_id = first_biz.get('id')
try:
    biz = queries.get_business_by_id(biz_id)
    if biz:
        print(f"✓ Retrieved business: {biz.get('name')}")
    else:
        print(f"✗ get_business_by_id({biz_id}) returned None")
except Exception as e:
    print(f"✗ Error in get_business_by_id: {e}")
    import traceback
    traceback.print_exc()

# Try to get deals for that business
print(f"\n3. GETTING DEALS FOR BUSINESS")
print("-" * 70)

try:
    deals = queries.get_deals_by_business(biz_id)
    print(f"✓ Retrieved {len(deals) if deals else 0} deals")
except Exception as e:
    print(f"✗ Error in get_deals_by_business: {e}")
    import traceback
    traceback.print_exc()

# Try to get reviews for that business
print(f"\n4. GETTING REVIEWS FOR BUSINESS")
print("-" * 70)

try:
    reviews = queries.get_reviews_for_business(biz_id)
    print(f"✓ Retrieved {len(reviews) if reviews else 0} reviews")
except Exception as e:
    print(f"✗ Error in get_reviews_for_business: {e}")
    import traceback
    traceback.print_exc()

# Try to get user's favorite business IDs (this was recently changed)
print(f"\n5. GETTING USER'S FAVORITE BUSINESS IDS")
print("-" * 70)

try:
    fav_ids = queries.get_favorite_business_ids(user_id)
    print(f"✓ Retrieved {len(fav_ids) if fav_ids else 0} favorites")
    print(f"  Type: {type(fav_ids)}")
except Exception as e:
    print(f"✗ Error in get_favorite_business_ids: {e}")
    import traceback
    traceback.print_exc()

print(f"\n" + "=" * 70)
print("DIAGNOSIS COMPLETE")
print("=" * 70)
