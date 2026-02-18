"""
Data access layer - all SQL operations.
Hidden Gems | FBLA 2026
"""
import sqlite3
import json
from .db import get_connection

# ---- Users ----
def user_by_email(email):
    """Get user row by email or None (includes email_verified, username)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE email = ?",
        (email.strip().lower(),)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def user_by_username(username):
    """Get user row by username or None."""
    if not username or not str(username).strip():
        return None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE username = ?",
        (username.strip().lower(),)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def user_by_email_or_username(identifier):
    """Get user by email or username. identifier is trimmed and lowercased for lookup."""
    if not identifier or not str(identifier).strip():
        return None
    key = identifier.strip().lower()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE lower(email) = ? OR lower(username) = ?",
        (key, key)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def get_user_by_id(user_id):
    """Get user row by ID or None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE id = ?",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def create_user(username, email, password_hash):
    """Insert a new user with email_verified=0. Returns new user id or None if email/username exists."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, email_verified) VALUES (?, ?, ?, 0)",
            (username.strip().lower(), email.strip().lower(), password_hash)
        )
        conn.commit()
        uid = cur.lastrowid
        conn.close()
        return uid
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return None


def set_email_verified(user_id, verified=1):
    """Mark user's email as verified."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET email_verified = ? WHERE id = ?", (verified, user_id))
    conn.commit()
    conn.close()


def update_user_username(user_id, new_username):
    """Update user's username."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET username = ? WHERE id = ?", (new_username.strip().lower(), user_id))
    conn.commit()
    conn.close()


def update_user_password(user_id, new_password_hash):
    """Update user's password hash."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password_hash = ? WHERE id = ?", (new_password_hash, user_id))
    conn.commit()
    conn.close()


def save_user_preferences(user_id, preferences_json):
    """Save user preferences (as JSON string) to database."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET user_preferences = ? WHERE id = ?", (preferences_json, user_id))
    conn.commit()
    conn.close()


def get_user_preferences(user_id):
    """Get user preferences (returns dict with favorite_categories, default_sort, etc.)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_preferences FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    
    if not row or not row[0]:
        # Return defaults if no preferences saved
        return {"favorite_categories": [], "default_sort": "name"}
    
    try:
        return json.loads(row[0])
    except (json.JSONDecodeError, TypeError):
        return {"favorite_categories": [], "default_sort": "name"}


def get_user_stats(user_id):
    """Get user statistics: total reviews, favorites, average rating given."""
    conn = get_connection()
    cur = conn.cursor()
    
    # Count reviews
    cur.execute("SELECT COUNT(*) FROM reviews WHERE user_id = ?", (user_id,))
    review_count = cur.fetchone()[0]
    
    # Count favorites
    cur.execute("SELECT COUNT(*) FROM favorites WHERE user_id = ?", (user_id,))
    favorite_count = cur.fetchone()[0]
    
    # Average rating given
    cur.execute("SELECT AVG(rating) FROM reviews WHERE user_id = ?", (user_id,))
    avg_rating = cur.fetchone()[0] or 0
    
    # Get user info with creation date
    cur.execute("SELECT created_date FROM users WHERE id = ?", (user_id,))
    user_row = cur.fetchone()
    created_date = user_row[0] if user_row else None
    
    conn.close()
    
    return {
        "review_count": review_count,
        "favorite_count": favorite_count,
        "avg_rating_given": round(avg_rating, 1) if avg_rating else 0,
        "created_date": created_date
    }


def create_email_verification_code(user_id, code):
    """Store a verification code for the user."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO email_verification_codes (user_id, code) VALUES (?, ?)",
        (user_id, code)
    )
    conn.commit()
    conn.close()


def get_latest_verification_code(user_id):
    """Get the most recent verification code for user, or None."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT code FROM email_verification_codes WHERE user_id = ? ORDER BY created_at DESC LIMIT 1",
        (user_id,)
    )
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def validate_email_code(user_id, code):
    """Check if code matches latest for user; if so set email_verified=1 and return True."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM email_verification_codes WHERE user_id = ? AND code = ? ORDER BY created_at DESC LIMIT 1",
        (user_id, code.strip())
    )
    row = cur.fetchone()
    if not row:
        conn.close()
        return False
    cur.execute("UPDATE users SET email_verified = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return True


# ---- Verification (for you to see in DB) ----
def log_verification_attempt(email, verification_type, question, correct_answer, user_answer, success, context):
    """Store every verification attempt in the verification_attempts table."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO verification_attempts
        (email, verification_type, question, correct_answer, user_answer, success, context)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (email or "", verification_type, question, correct_answer, user_answer or "", 1 if success else 0, context))
    conn.commit()
    conn.close()


def get_all_verification_attempts():
    """Return all verification attempts (for admin/view)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM verification_attempts ORDER BY attempted_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---- Businesses ----
def get_all_businesses():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM businesses ORDER BY name")
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_businesses_by_category(category):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM businesses WHERE category = ? ORDER BY name", (category,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_businesses_for_directory(category=None, sort_by="name"):
    """
    Get businesses optionally filtered by category, sorted.
    sort_by: 'name' | 'rating_high' | 'rating_low' | 'reviews' | 'reviews_low'
    """
    if category and str(category).strip() and str(category).strip().lower() != "all":
        rows = get_businesses_by_category(category.strip())
    else:
        rows = get_all_businesses()
    if sort_by == "rating_high":
        rows = sorted(rows, key=lambda b: (float(b.get("average_rating") or 0), b.get("name") or ""), reverse=True)
    elif sort_by == "rating_low":
        rows = sorted(rows, key=lambda b: (float(b.get("average_rating") or 0), b.get("name") or ""))
    elif sort_by == "reviews":
        rows = sorted(rows, key=lambda b: (int(b.get("total_reviews") or 0), b.get("name") or ""), reverse=True)
    elif sort_by == "reviews_low":
        rows = sorted(rows, key=lambda b: (int(b.get("total_reviews") or 0), b.get("name") or ""))
    else:
        rows = sorted(rows, key=lambda b: (b.get("name") or "").lower())
    return rows


def get_business_by_id(bid):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM businesses WHERE id = ?", (bid,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None


def search_businesses_by_name(query):
    """Search businesses by name (case-insensitive partial match)."""
    if not query or not str(query).strip():
        return get_all_businesses()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM businesses WHERE lower(name) LIKE ? ORDER BY name",
        ("%" + query.strip().lower() + "%",)
    )
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_categories():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM businesses ORDER BY category")
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_all_business_names():
    """Set of lowercase business names (for dedupe when syncing from API)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT name FROM businesses")
    rows = cur.fetchall()
    conn.close()
    return {r[0].lower().strip() for r in rows}


def get_business_id_by_name(name):
    """Get business id by exact name match (case-insensitive). Returns None if not found."""
    if not name or not str(name).strip():
        return None
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM businesses WHERE lower(trim(name)) = ?", (name.strip().lower(),))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else None


def update_business(business_id, category=None, description=None, address=None, average_rating=None, total_reviews=None, phone=None, website=None, yelp_url=None, latitude=None, longitude=None, price_range=None, hours=None, photo_url=None, attributes=None, summary=None, yelp_id=None):
    """Update business fields. None means leave unchanged."""
    conn = get_connection()
    cur = conn.cursor()
    # Build dynamic update
    updates = []
    args = []
    
    field_mapping = {
        'category': category,
        'description': description,
        'address': address,
        'average_rating': average_rating,
        'total_reviews': total_reviews,
        'phone': phone,
        'website': website,
        'yelp_url': yelp_url,
        'latitude': latitude,
        'longitude': longitude,
        'price_range': price_range,
        'hours': hours,
        'photo_url': photo_url,
        'attributes': attributes,
        'summary': summary,
        'yelp_id': yelp_id,
    }
    
    for field, value in field_mapping.items():
        if value is not None:
            updates.append(f"{field} = ?")
            args.append(value)
    
    if not updates:
        conn.close()
        return
    args.append(business_id)
    cur.execute("UPDATE businesses SET " + ", ".join(updates) + " WHERE id = ?", args)
    conn.commit()
    conn.close()


def insert_business(name, category, description, average_rating=0, total_reviews=0, address=None, phone=None, website=None, yelp_url=None, latitude=None, longitude=None, price_range=None, hours=None, photo_url=None, attributes=None, summary=None, yelp_id=None):
    """Insert one business with all available fields. Returns new id."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO businesses (name, category, description, address, average_rating, total_reviews, 
           phone, website, yelp_url, latitude, longitude, price_range, hours, photo_url, attributes, summary, yelp_id) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (name, category, description, address or "", average_rating, total_reviews, 
         phone or "", website or "", yelp_url or "", latitude, longitude, price_range or "", 
         hours or "", photo_url or "", attributes or "", summary or "", yelp_id or "")
    )
    conn.commit()
    bid = cur.lastrowid
    conn.close()
    return bid


# ---- Deals ----
def get_deals_by_business(business_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM deals WHERE business_id = ?", (business_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_deals():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.*, b.name AS business_name
        FROM deals d
        JOIN businesses b ON d.business_id = b.id
        ORDER BY b.name
    """)
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---- Reviews ----
def add_review(business_id, user_id, rating, review_text, created_date, created_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reviews (business_id, user_id, rating, review_text, created_date, created_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (business_id, user_id, rating, review_text, created_date, created_time))
    conn.commit()
    rid = cur.lastrowid
    # Update business average rating and count
    cur.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE business_id = ?", (business_id,))
    avg, count = cur.fetchone()
    cur.execute("UPDATE businesses SET average_rating = ?, total_reviews = ? WHERE id = ?",
                (round(avg, 2) if avg else 0, count or 0, business_id))
    conn.commit()
    conn.close()
    return rid


def get_reviews_for_business(business_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, u.email, u.username
        FROM reviews r
        JOIN users u ON r.user_id = u.id
        WHERE r.business_id = ?
        ORDER BY r.created_date DESC, r.created_time DESC
    """, (business_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_reviews_by_user(user_id):
    """All reviews written by this user (for My Reviews screen)."""
    if not user_id:
        return []
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT r.*, b.name AS business_name
        FROM reviews r
        JOIN businesses b ON r.business_id = b.id
        WHERE r.user_id = ?
        ORDER BY r.created_date DESC, r.created_time DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_trending_businesses(limit=20):
    """Top businesses by rating and by review count (popular/trending)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM businesses
        ORDER BY average_rating DESC, total_reviews DESC
        LIMIT ?
    """, (limit * 2,))
    rows = cur.fetchall()
    conn.close()
    seen = set()
    result = []
    for r in rows:
        d = dict(r)
        bid = d.get("id")
        if bid in seen:
            continue
        seen.add(bid)
        result.append(d)
        if len(result) >= limit:
            break
    return result


def get_business_ids_with_deals():
    """Set of business IDs that have at least one deal."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT business_id FROM deals")
    rows = cur.fetchall()
    conn.close()
    return {r[0] for r in rows}


# ---- Favorites ----
def add_favorite(user_id, business_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO favorites (user_id, business_id) VALUES (?, ?)", (user_id, business_id))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.rollback()
        conn.close()
        return False  # already favorited


def remove_favorite(user_id, business_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM favorites WHERE user_id = ? AND business_id = ?", (user_id, business_id))
    conn.commit()
    conn.close()


def get_favorite_business_ids(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT business_id FROM favorites WHERE user_id = ?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_favorite_businesses(user_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT b.* FROM businesses b
        JOIN favorites f ON b.id = f.business_id
        WHERE f.user_id = ?
        ORDER BY b.name
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_recommended_businesses(user_id, limit=20):
    """Recommend businesses: from user's favorite categories (highest rated), then most popular overall."""
    favs = get_favorite_businesses(user_id) if user_id else []
    categories = list({b["category"] for b in favs if b.get("category")})
    conn = get_connection()
    cur = conn.cursor()
    seen_ids = set()
    result = []
    if categories:
        placeholders = ",".join("?" * len(categories))
        cur.execute(f"""
            SELECT * FROM businesses
            WHERE category IN ({placeholders}) AND id NOT IN (SELECT business_id FROM favorites WHERE user_id = ?)
            ORDER BY average_rating DESC, total_reviews DESC
            LIMIT ?
        """, (*categories, user_id, limit))
        for row in cur.fetchall():
            d = dict(row)
            if d["id"] not in seen_ids:
                seen_ids.add(d["id"])
                result.append(d)
    if len(result) < limit:
        cur.execute("""
            SELECT * FROM businesses
            WHERE id NOT IN (SELECT business_id FROM favorites WHERE user_id = ?)
            ORDER BY average_rating DESC, total_reviews DESC
            LIMIT ?
        """, (user_id, limit - len(result)))
        for row in cur.fetchall():
            d = dict(row)
            if d["id"] not in seen_ids:
                seen_ids.add(d["id"])
                result.append(d)
    conn.close()
    return result[:limit]
