"""
Seed database with default user and sample businesses/deals.
Uses Yelp API for Richmond, VA businesses when YELP_API_KEY is set.
Hidden Gems | FBLA 2026
"""
from .db import get_connection
from . import queries
from ..logic.auth import hash_password

# Names of static seed businesses; removed when we have Yelp data so only real Richmond businesses show
STATIC_BUSINESS_NAMES = {
    "Mama's Kitchen", "Tech Fix Pro", "Green Leaf Cafe", "Style Corner", "Sunset Cinema",
    "Wellness Plus", "Joe's Pizza", "Book Nook", "FitLife Gym", "Quick Clean",
}


def _remove_static_seed_businesses():
    """Remove known static seed businesses so only Yelp (real Richmond) businesses remain."""
    conn = get_connection()
    cur = conn.cursor()
    for name in STATIC_BUSINESS_NAMES:
        cur.execute("DELETE FROM deals WHERE business_id IN (SELECT id FROM businesses WHERE name = ?)", (name,))
        cur.execute("DELETE FROM reviews WHERE business_id IN (SELECT id FROM businesses WHERE name = ?)", (name,))
        cur.execute("DELETE FROM favorites WHERE business_id IN (SELECT id FROM businesses WHERE name = ?)", (name,))
        cur.execute("DELETE FROM businesses WHERE name = ?", (name,))
    conn.commit()
    conn.close()


def _sync_richmond_from_yelp():
    """Fetch Richmond, VA businesses from Yelp API; insert new ones and update existing (by name). Returns (added, updated)."""
    try:
        from ..logic.yelp_api import fetch_richmond_businesses, is_configured
    except ImportError:
        return 0, 0
    if not is_configured():
        return 0, 0
    rows = fetch_richmond_businesses(max_per_category=50)
    # When we have Yelp data, remove static seed businesses so only real Richmond businesses show
    if rows:
        _remove_static_seed_businesses()
    added = 0
    updated = 0
    for row in rows:
        bid = queries.get_business_id_by_name(row["name"])
        if bid:
            queries.update_business(
                bid,
                category=row.get("category"),
                description=row.get("description"),
                address=row.get("address"),
                average_rating=row.get("average_rating"),
                total_reviews=row.get("total_reviews"),
                phone=row.get("phone"),
                website=row.get("website"),
                yelp_url=row.get("yelp_url"),
                latitude=row.get("latitude"),
                longitude=row.get("longitude"),
                price_range=row.get("price_range"),
                hours=row.get("hours"),
                photo_url=row.get("photo_url"),
                attributes=row.get("attributes"),
                summary=row.get("summary"),
                yelp_id=row.get("yelp_id"),
            )
            updated += 1
        else:
            queries.insert_business(
                name=row["name"],
                category=row.get("category"),
                description=row.get("description"),
                average_rating=row.get("average_rating", 0),
                total_reviews=row.get("total_reviews", 0),
                address=row.get("address"),
                phone=row.get("phone"),
                website=row.get("website"),
                yelp_url=row.get("yelp_url"),
                latitude=row.get("latitude"),
                longitude=row.get("longitude"),
                price_range=row.get("price_range"),
                hours=row.get("hours"),
                photo_url=row.get("photo_url"),
                attributes=row.get("attributes"),
                summary=row.get("summary"),
                yelp_id=row.get("yelp_id"),
            )
            added += 1
    return added, updated


def ensure_seed_data():
    """Create demo user; fill businesses from Yelp (Richmond VA) if API key set, else static seed."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, email, password_hash, email_verified) VALUES (?, ?, ?, 1)",
            ("demo", "demo@hiddengems.local", hash_password("demo1234"))
        )
        conn.commit()
    conn.close()

    # Businesses: try Yelp (Richmond, VA) first; add new and update existing
    _sync_richmond_from_yelp()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM businesses")
    count = cur.fetchone()[0]
    conn.close()
    if count == 0:
        # Fallback: static seed when Yelp not configured or returned nothing
        _seed_static_businesses()


def _seed_static_businesses():
    """Static Richmond-style businesses when Yelp is not used."""
    conn = get_connection()
    cur = conn.cursor()
    businesses = [
        ("Mama's Kitchen", "Food", "Homestyle comfort food and daily specials.", 4.5, 12),
        ("Tech Fix Pro", "Services", "Computer and phone repair, same-day service.", 4.8, 28),
        ("Green Leaf Cafe", "Food", "Organic coffee and light bites.", 4.2, 8),
        ("Style Corner", "Retail", "Trendy clothing and accessories.", 4.0, 15),
        ("Sunset Cinema", "Entertainment", "Independent films and classic screenings.", 4.6, 22),
        ("Wellness Plus", "Health and Wellness", "Massage, yoga, and nutrition counseling.", 4.7, 18),
        ("Joe's Pizza", "Food", "New York-style pizza and subs.", 4.3, 31),
        ("Book Nook", "Retail", "Used and new books, cozy reading space.", 4.4, 9),
        ("FitLife Gym", "Health and Wellness", "24/7 gym with classes and personal training.", 4.1, 45),
        ("Quick Clean", "Services", "Residential and commercial cleaning.", 4.5, 14),
    ]
    for name, category, desc, rating, count in businesses:
        cur.execute(
            "INSERT INTO businesses (name, category, description, address, average_rating, total_reviews) VALUES (?, ?, ?, ?, ?, ?)",
            (name, category, desc, None, rating, count)
        )
    conn.commit()
    # Add some deals
    cur.execute("SELECT id FROM businesses WHERE name = 'Mama''s Kitchen'")
    bid = cur.fetchone()[0]
    cur.execute("INSERT INTO deals (business_id, description) VALUES (?, ?)", (bid, "10% off lunch Monday–Friday"))
    cur.execute("SELECT id FROM businesses WHERE name = 'Tech Fix Pro'")
    bid = cur.fetchone()[0]
    cur.execute("INSERT INTO deals (business_id, description) VALUES (?, ?)", (bid, "Free diagnostic on first visit"))
    cur.execute("SELECT id FROM businesses WHERE name = 'Green Leaf Cafe'")
    bid = cur.fetchone()[0]
    cur.execute("INSERT INTO deals (business_id, description) VALUES (?, ?)", (bid, "Buy 2 coffees, get 1 free"))
    cur.execute("SELECT id FROM businesses WHERE name = 'Joe''s Pizza'")
    bid = cur.fetchone()[0]
    cur.execute("INSERT INTO deals (business_id, description) VALUES (?, ?)", (bid, "Large pizza for the price of medium on Tuesdays"))
    conn.commit()
    conn.close()


def refresh_richmond_from_yelp():
    """Fetch latest Richmond, VA businesses from Yelp; add new and update existing. Returns (added, updated)."""
    return _sync_richmond_from_yelp()


def replace_all_with_yelp():
    """
    Delete ALL current businesses and load only from Yelp (Richmond, VA).
    Use this to switch from static/fake businesses to real API businesses.
    Returns (number_loaded, None) on success, or (0, error_message) on failure.
    """
    try:
        from ..logic.yelp_api import fetch_richmond_businesses, is_configured, get_last_error
    except ImportError:
        return 0, "Yelp module not found"
    if not is_configured():
        return 0, "YELP_API_KEY not set in config.py"
    rows = fetch_richmond_businesses(max_per_category=50)
    err = get_last_error()
    if not rows:
        return 0, (err or "Yelp returned no businesses. Check your API key and internet.")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM deals")
    cur.execute("DELETE FROM reviews")
    cur.execute("DELETE FROM favorites")
    cur.execute("DELETE FROM businesses")
    conn.commit()
    conn.close()
    for row in rows:
        queries.insert_business(
            name=row["name"],
            category=row["category"],
            description=row["description"],
            average_rating=row["average_rating"],
            total_reviews=row["total_reviews"],
            address=row.get("address"),
        )
    return len(rows), None
