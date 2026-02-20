"""
Data access layer - all SQL operations.
Hidden Gems | FBLA 2026
"""
import sqlite3
import json
from .db import get_connection

# ===== USER MANAGEMENT ===== 
# All functions for retrieving and managing user account data

def user_by_email(email_address):
    """
    Retrieve user account by email address.
    
    Email is normalized (stripped, lowercased) for consistent lookups.
    
    Args:
        email_address (str): Email to search for
    
    Returns:
        dict: User record with keys (id, email, password_hash, email_verified, username)
        None: If no user found with this email
    """
    conn = get_connection()
    cur = conn.cursor()
    # Normalize email: trim whitespace and convert to lowercase
    normalized_email = email_address.strip().lower()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE email = ?",
        (normalized_email,)
    )
    user_row = cur.fetchone()
    conn.close()
    # Convert SQLite Row object to dictionary for easier access
    return dict(user_row) if user_row else None


def user_by_username(username_input):
    """
    Retrieve user account by username.
    
    Username is normalized (stripped, lowercased) for consistent lookups.
    Case-insensitive search for better user experience.
    
    Args:
        username_input (str): Username to search for
    
    Returns:
        dict: User record with keys (id, email, password_hash, email_verified, username)
        None: If username is empty or no user found
    """
    # Validate input is provided
    if not username_input or not str(username_input).strip():
        return None
    
    conn = get_connection()
    cur = conn.cursor()
    # Normalize username: trim whitespace and convert to lowercase
    normalized_username = username_input.strip().lower()
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE username = ?",
        (normalized_username,)
    )
    user_row = cur.fetchone()
    conn.close()
    # Convert SQLite Row object to dictionary
    return dict(user_row) if user_row else None


def user_by_email_or_username(user_identifier):
    """
    Retrieve user by either email address or username (flexible lookup).
    
    This is useful for login forms where users might enter either their email or username.
    Normalized for case-insensitive matching.
    
    Args:
        user_identifier (str): Email address or username to search for
    
    Returns:
        dict: User record with keys (id, email, password_hash, email_verified, username)
        None: If identifier is empty or no user found
    """
    # Validate input is provided
    if not user_identifier or not str(user_identifier).strip():
        return None
    
    # Normalize identifier: trim and lowercase for case-insensitive matching
    normalized_key = user_identifier.strip().lower()
    
    conn = get_connection()
    cur = conn.cursor()
    # Query uses OR condition: match by email OR username (both case-insensitive)
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE lower(email) = ? OR lower(username) = ?",
        (normalized_key, normalized_key)
    )
    user_row = cur.fetchone()
    conn.close()
    # Convert SQLite Row object to dictionary
    return dict(user_row) if user_row else None


def get_user_by_id(user_id_value):
    """
    Retrieve user account by user ID.
    
    This is the fastest lookup method (queries by primary key).
    Returns complete user record for authenticated session management.
    
    Args:
        user_id_value (int): User ID from users table primary key
    
    Returns:
        dict: User record with keys (id, email, password_hash, email_verified, username)
        None: If no user found with this ID
    """
    conn = get_connection()
    cur = conn.cursor()
    # Query by primary key (fastest database lookup)
    cur.execute(
        "SELECT id, email, password_hash, email_verified, username FROM users WHERE id = ?",
        (user_id_value,)
    )
    user_row = cur.fetchone()
    conn.close()
    # Convert SQLite Row object to dictionary
    return dict(user_row) if user_row else None


def create_user(username_new, email_new, password_hash_value):
    """
    Create a new user account after validation.
    
    New users start with email_verified=0 (must verify email before login).
    Enforces unique constraints on username and email (returns None if duplicate).
    
    Args:
        username_new (str): Normalized username (already lowercased by auth module)
        email_new (str): Normalized email (already lowercased by auth module)
        password_hash_value (str): SHA-256 hash of password (computed by auth module)
    
    Returns:
        int: New user ID if creation successful
        None: If username or email already exists (IntegrityError)
    """
    conn = get_connection()
    cur = conn.cursor()
    try:
        # Insert new user with email_verified=0 (unverified)
        cur.execute(
            "INSERT INTO users (username, email, password_hash, email_verified) VALUES (?, ?, ?, 0)",
            (username_new.strip().lower(), email_new.strip().lower(), password_hash_value)
        )
        conn.commit()
        # Get the auto-generated user ID (primary key)
        new_user_id = cur.lastrowid
        conn.close()
        return new_user_id
    except sqlite3.IntegrityError:
        # Unique constraint violated (email or username already exists)
        conn.rollback()
        conn.close()
        return None  # Signal creation failed due to duplicate


def set_email_verified(user_id_to_mark, is_verified_flag=1):
    """
    Mark a user's email address as verified (or unverified).
    
    Called after user confirms verification code sent to their email.
    Users cannot log in without email_verified=1.
    
    Args:
        user_id_to_mark (int): User ID to update
        is_verified_flag (int): 1 = verified, 0 = unverified (default: 1 for verified)
    
    Returns:
        None (database is updated immediately)
    """
    conn = get_connection()
    cur = conn.cursor()
    # Update email_verified flag in users table
    cur.execute(
        "UPDATE users SET email_verified = ? WHERE id = ?",
        (is_verified_flag, user_id_to_mark)
    )
    conn.commit()
    conn.close()


def update_user_username(user_id_to_update, new_username_value):
    """
    Update a user's username in their account.
    
    Called from settings page when user changes their username.
    Username is normalized (lowercased) for consistency.
    
    Args:
        user_id_to_update (int): User ID to update
        new_username_value (str): New username (will be lowercased)
    
    Returns:
        None (database is updated immediately)
    """
    conn = get_connection()
    cur = conn.cursor()
    # Normalize username and update in database
    cur.execute(
        "UPDATE users SET username = ? WHERE id = ?",
        (new_username_value.strip().lower(), user_id_to_update)
    )
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
    verification_row = cur.fetchone()
    conn.close()
    return verification_row[0] if verification_row else None


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
    attempt_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in attempt_rows]


# ===== BUSINESS LOOKUP & SEARCH =====
# All functions for retrieving, searching, and managing business data from directory

def get_all_businesses():
    """
    Retrieve all businesses in the directory (sorted alphabetically).
    
    Returns complete business records including ratings, reviews, photos, hours, etc.
    
    Returns:
        list: List of business dictionaries, each with complete business data
        Returns [] if no businesses in database
    """
    conn = get_connection()
    cur = conn.cursor()
    # Query all businesses, sorted by name for consistent display
    cur.execute("SELECT * FROM businesses ORDER BY name")
    business_rows = cur.fetchall()
    conn.close()
    # Convert SQLite Row objects to dictionaries
    return [dict(business_row) for business_row in business_rows]


def get_businesses_by_category(category_name):
    """
    Retrieve all businesses in a specific category.
    
    Categories include: Food, Retail, Services, Entertainment, Health & Wellness
    
    Args:
        category_name (str): Category to filter by
    
    Returns:
        list: List of business dictionaries in that category, sorted by name
        Returns [] if no businesses in that category
    """
    conn = get_connection()
    cur = conn.cursor()
    # Filter by exact category match, sorted alphabetically
    cur.execute(
        "SELECT * FROM businesses WHERE category = ? ORDER BY name",
        (category_name,)
    )
    business_rows = cur.fetchall()
    conn.close()
    # Convert SQLite Row objects to dictionaries
    return [dict(business_row) for business_row in business_rows]


def get_businesses_for_directory(category_filter=None, sort_by_option="name"):
    """
    Get businesses for directory page with optional filtering and sorting.
    
    Combines category filtering with multiple sort options to support
    different ways users browse the business directory.
    
    Args:
        category_filter (str): Optional category to filter by. If None, \"all\", or empty,
                               returns all businesses regardless of category.
        sort_by_option (str): How to sort results:
                              - 'name' (default) - Alphabetical by business name
                              - 'rating_high' - Highest rated first (4.5+ stars)
                              - 'rating_low' - Lowest rated first
                              - 'reviews' - Most reviewed first (most popular)
                              - 'reviews_low' - Least reviewed first (hidden gems)
    
    Returns:
        list: List of business dictionaries, filtered and sorted as requested
    """
    # Apply category filter if specified
    if category_filter and str(category_filter).strip() and str(category_filter).strip().lower() != "all":
        filtered_businesses = get_businesses_by_category(category_filter.strip())
    else:
        # No filter: retrieve all businesses
        filtered_businesses = get_all_businesses()
    
    # Apply sort option
    if sort_by_option == "rating_high":
        # Highest rated first (4.5+ stars) - best businesses
        filtered_businesses = sorted(
            filtered_businesses,
            key=lambda b: (float(b.get("average_rating") or 0), b.get("name") or ""),
            reverse=True
        )
    elif sort_by_option == "rating_low":
        # Lowest rated first - discover underrated businesses
        filtered_businesses = sorted(
            filtered_businesses,
            key=lambda b: (float(b.get("average_rating") or 0), b.get("name") or "")
        )
    elif sort_by_option == "reviews":
        # Most reviewed first - most popular/established businesses
        filtered_businesses = sorted(
            filtered_businesses,
            key=lambda b: (int(b.get("total_reviews") or 0), b.get("name") or ""),
            reverse=True
        )
    elif sort_by_option == "reviews_low":
        # Least reviewed first - actually hidden gems
        filtered_businesses = sorted(
            filtered_businesses,
            key=lambda b: (int(b.get("total_reviews") or 0), b.get("name") or "")
        )
    else:
        # Default: alphabetical by name (case-insensitive)
        filtered_businesses = sorted(
            filtered_businesses,
            key=lambda b: (b.get("name") or "").lower()
        )
    
    return filtered_businesses


def get_business_by_id(business_id_to_fetch):
    """
    Retrieve a single business record by its unique ID.
    
    Used for business detail pages where we need all information about one business.
    
    Args:
        business_id_to_fetch (int): Business ID (primary key)
    
    Returns:
        dict: Complete business record (name, category, rating, reviews, hours, photos, etc.)
        None: If no business found with this ID
    """
    conn = get_connection()
    cur = conn.cursor()
    # Query single business by primary key (fastest lookup)
    cur.execute("SELECT * FROM businesses WHERE id = ?", (business_id_to_fetch,))
    business_row = cur.fetchone()
    conn.close()
    # Convert SQLite Row object to dictionary
    return dict(business_row) if business_row else None


def search_businesses_by_name(search_query):
    """
    Search the business directory for businesses matching a search term.
    
    Uses case-insensitive partial matching (LIKE query) so users can search
    for "pizza" and find "Mario's Pizza Place", "Pizza Hut", etc.
    
    Args:
        search_query (str): Search term to find (e.g., "coffee", "pizza", "gym")
    
    Returns:
        list: List of matching business dictionaries, sorted alphabetically by name
        Returns all businesses if query is empty/None (no filter applied)
    """
    # If no search query provided, return all businesses
    if not search_query or not str(search_query).strip():
        return get_all_businesses()
    
    conn = get_connection()
    cur = conn.cursor()
    # Use LIKE with wildcards for partial, case-insensitive matching
    cur.execute(
        "SELECT * FROM businesses WHERE lower(name) LIKE ? ORDER BY name",
        ("%" + search_query.strip().lower() + "%",)  # Wildcards on both sides
    )
    business_rows = cur.fetchall()
    conn.close()
    # Convert SQLite Row objects to dictionaries
    return [dict(business_row) for business_row in business_rows]


def get_categories():
    """
    Retrieve all unique business categories present in the directory.
    
    Returns list of category names for filtering in directory page.
    Categories include: Food, Retail, Services, Entertainment, Health & Wellness
    
    Returns:
        list: List of unique category strings, sorted alphabetically
        Example: ["Entertainment", "Food", "Health and Wellness", "Retail", "Services"]
    """
    conn = get_connection()
    cur = conn.cursor()
    # Query all unique categories from businesses table, sorted
    cur.execute("SELECT DISTINCT category FROM businesses ORDER BY category")
    category_rows = cur.fetchall()
    conn.close()
    # Extract category name from each row tuple (only first column)
    return [category_name[0] for category_name in category_rows]


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
    update_clauses = []
    parameters = []
    
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
            update_clauses.append(f"{field} = ?")
            parameters.append(value)
    
    if not update_clauses:
        conn.close()
        return
    parameters.append(business_id)
    cur.execute("UPDATE businesses SET " + ", ".join(update_clauses) + " WHERE id = ?", parameters)
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
    business_id = cur.lastrowid
    conn.close()
    return business_id


# ---- Deals ----
def get_deals_by_business(business_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM deals WHERE business_id = ?", (business_id,))
    deal_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in deal_rows]


def get_all_deals():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT d.*, b.name AS business_name
        FROM deals d
        JOIN businesses b ON d.business_id = b.id
        ORDER BY b.name
    """)
    deal_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in deal_rows]


# ---- Reviews ----
def add_review(business_id, user_id, rating, review_text, created_date, created_time):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reviews (business_id, user_id, rating, review_text, created_date, created_time)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (business_id, user_id, rating, review_text, created_date, created_time))
    conn.commit()
    review_id = cur.lastrowid
    # Update business average rating and count
    cur.execute("SELECT AVG(rating), COUNT(*) FROM reviews WHERE business_id = ?", (business_id,))
    avg, count = cur.fetchone()
    cur.execute("UPDATE businesses SET average_rating = ?, total_reviews = ? WHERE id = ?",
                (round(avg, 2) if avg else 0, count or 0, business_id))
    conn.commit()
    conn.close()
    return review_id


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
    review_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in review_rows]


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
    review_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in review_rows]


def get_trending_businesses(limit=20):
    """Top businesses by rating and by review count (popular/trending)."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT * FROM businesses
        ORDER BY average_rating DESC, total_reviews DESC
        LIMIT ?
    """, (limit * 2,))
    business_rows = cur.fetchall()
    conn.close()
    seen_business_ids = set()
    trending_businesses = []
    for row in business_rows:
        business = dict(row)
        business_id = business.get("id")
        if business_id in seen_business_ids:
            continue
        seen_business_ids.add(business_id)
        trending_businesses.append(business)
        if len(trending_businesses) >= limit:
            break
    return trending_businesses


def get_business_ids_with_deals():
    """Set of business IDs that have at least one deal."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT business_id FROM deals")
    deal_rows = cur.fetchall()
    conn.close()
    return {r[0] for r in deal_rows}


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
    favorite_rows = cur.fetchall()
    conn.close()
    return [dict(r) for r in favorite_rows]


def get_recommended_businesses(user_id, limit=20):
    """Recommend businesses: from user's favorite categories (highest rated), then most popular overall."""
    favorites = get_favorite_businesses(user_id) if user_id else []
    categories = list({business["category"] for business in favorites if business.get("category")})
    conn = get_connection()
    cur = conn.cursor()
    seen_business_ids = set()
    recommended_businesses = []
    if categories:
        placeholders = ",".join("?" * len(categories))
        cur.execute(f"""
            SELECT * FROM businesses
            WHERE category IN ({placeholders}) AND id NOT IN (SELECT business_id FROM favorites WHERE user_id = ?)
            ORDER BY average_rating DESC, total_reviews DESC
            LIMIT ?
        """, (*categories, user_id, limit))
        for row in cur.fetchall():
            business = dict(row)
            if business["id"] not in seen_business_ids:
                seen_business_ids.add(business["id"])
                recommended_businesses.append(business)
    if len(recommended_businesses) < limit:
        cur.execute("""
            SELECT * FROM businesses
            WHERE id NOT IN (SELECT business_id FROM favorites WHERE user_id = ?)
            ORDER BY average_rating DESC, total_reviews DESC
            LIMIT ?
        """, (user_id, limit - len(recommended_businesses)))
        for row in cur.fetchall():
            business = dict(row)
            if business["id"] not in seen_business_ids:
                seen_business_ids.add(business["id"])
                recommended_businesses.append(business)
    conn.close()
    return recommended_businesses[:limit]
