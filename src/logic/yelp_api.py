"""
Fetch small businesses in Richmond, VA from Yelp Fusion API.
Hidden Gems | FBLA 2026
https://www.yelp.com/developers/v3/manage_app
"""
import os
import json
import urllib.request
import urllib.parse
import urllib.error

LOCATION = "Richmond, VA"
BASE_URL = "https://api.yelp.com/v3/businesses/search"

# Map Yelp category aliases to our app categories (Food, Retail, Services, Entertainment, Health and Wellness)
YELP_TO_APP_CATEGORY = {
    "food": "Food",
    "restaurants": "Food",
    "coffee": "Food",
    "bakeries": "Food",
    "delis": "Food",
    "pizza": "Food",
    "sandwiches": "Food",
    "shopping": "Retail",
    "retail": "Retail",
    "clothing": "Retail",
    "bookstores": "Retail",
    "homeservices": "Services",
    "localservices": "Services",
    "plumbing": "Services",
    "electricians": "Services",
    "autorepair": "Services",
    "laundry": "Services",
    "banks": "Services",
    "professional": "Services",
    "nightlife": "Entertainment",
    "arts": "Entertainment",
    "theater": "Entertainment",
    "museums": "Entertainment",
    "bowling": "Entertainment",
    "movietheaters": "Entertainment",
    "gyms": "Health and Wellness",
    "fitness": "Health and Wellness",
    "health": "Health and Wellness",
    "spas": "Health and Wellness",
    "beautysvc": "Health and Wellness",
    "massage": "Health and Wellness",
    "nutrition": "Health and Wellness",
}


def _get_api_key():
    """Get Yelp API key from config.py or environment."""
    try:
        import config
        key = getattr(config, "YELP_API_KEY", None) or os.environ.get("YELP_API_KEY", "").strip()
        return key if key else None
    except ImportError:
        return os.environ.get("YELP_API_KEY", "").strip() or None


# Store last error for UI to display
_last_error = None


def _request(offset=0, limit=50, term=None, categories=None):
    """Make one request to Yelp Business Search. Returns (data, None) or (None, error_message)."""
    global _last_error
    _last_error = None
    api_key = _get_api_key()
    if not api_key:
        _last_error = "YELP_API_KEY not set in config.py"
        return None, _last_error
    params = {
        "location": LOCATION,
        "limit": limit,
        "offset": offset,
        "sort_by": "rating",
    }
    if term:
        params["term"] = term
    if categories:
        params["categories"] = categories
    url = BASE_URL + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode()), None
    except urllib.error.HTTPError as e:
        _last_error = f"Yelp API error: {e.code} {e.reason}"
        try:
            body = e.read().decode()[:200]
            _last_error += " — " + body
        except Exception:
            pass
        return None, _last_error
    except urllib.error.URLError as e:
        _last_error = f"Network error: {e.reason}"
        return None, _last_error
    except Exception as e:
        _last_error = str(e)
        return None, _last_error


def get_last_error():
    """Return last Yelp API error message, or None."""
    return _last_error


def _yelp_category_to_app(yelp_categories):
    """Map Yelp category list to our app category (Food, Retail, etc.)."""
    if not yelp_categories:
        return "Retail"
    for category_entry in yelp_categories:
        alias = (category_entry.get("alias") or "").lower()
        if alias in YELP_TO_APP_CATEGORY:
            return YELP_TO_APP_CATEGORY[alias]
    return "Retail"


def _generate_business_summary(name, category, price_range, attributes, rating, review_count):
    """Generate an intelligent summary from business attributes and rating."""
    summary_parts = []
    
    # Quality indicator based on rating
    if rating >= 4.5:
        summary_parts.append("Highly-rated")
    elif rating >= 4.0:
        summary_parts.append("Well-reviewed")
    elif rating >= 3.5:
        summary_parts.append("Popular")
    
    # Price range
    if price_range:
        price_symbols = price_range.count("$")
        if price_symbols == 1:
            summary_parts.append("budget-friendly")
        elif price_symbols == 2:
            summary_parts.append("moderate pricing")
        elif price_symbols >= 3:
            summary_parts.append("upscale")
    
    # Attributes-based features
    if isinstance(attributes, dict):
        if attributes.get("caters_to_vegans"):
            summary_parts.append("vegan options")
        if attributes.get("good_for_groups"):
            summary_parts.append("great for groups")
        if attributes.get("good_for_kids"):
            summary_parts.append("family-friendly")
        if attributes.get("outdoor_seating"):
            summary_parts.append("outdoor seating")
        if attributes.get("wifi"):
            summary_parts.append("WiFi available")
        if attributes.get("parking"):
            summary_parts.append("has parking")
        if attributes.get("wheelchair_accessible"):
            summary_parts.append("wheelchair accessible")
        if attributes.get("dogs_allowed"):
            summary_parts.append("dogs welcome")
    
    # Review popularity
    if review_count > 500:
        summary_parts.append("very popular")
    elif review_count > 200:
        summary_parts.append("well-established")
    
    if summary_parts:
        return f"{name} - {', '.join(summary_parts)}."
    else:
        return f"{name} - A {category.lower()} business in Richmond with {review_count} reviews and {rating} rating."



def _business_to_row(b):
    """Convert one Yelp business object to our schema; includes all available Yelp data."""
    name = (b.get("name") or "Unknown").strip()
    if not name:
        return None
    rating = float(b.get("rating") or 0)
    review_count = int(b.get("review_count") or 0)
    categories = b.get("categories") or []
    category = _yelp_category_to_app(categories)
    location_data = b.get("location") or {}
    city = location_data.get("city") or "Richmond"
    state = location_data.get("state") or "VA"
    zip_code = location_data.get("zip_code") or ""
    
    # Address
    display_address = location_data.get("display_address")
    if isinstance(display_address, list) and display_address:
        address = ", ".join(str(x).strip() for x in display_address if x)
    else:
        address = ", ".join(filter(None, [location_data.get("address1"), city, state, zip_code]))
    
    # Basic description
    description = f"Local {category.lower()} in {city}, VA."
    if address:
        description += " " + address
    
    # Extract all new fields
    phone = b.get("phone", "") or ""
    website = b.get("url", "") or ""
    latitude = b.get("coordinates", {}).get("latitude")
    longitude = b.get("coordinates", {}).get("longitude")
    yelp_url = b.get("url", "")
    price_range = b.get("price", "") or ""
    photo_url = b.get("image_url", "") or ""
    yelp_id = b.get("id", "") or ""
    
    # Format hours (open_now will be in hours array)
    hours_data = b.get("hours", [])
    hours_text = ""
    if hours_data and isinstance(hours_data, list) and len(hours_data) > 0:
        hours_entries = hours_data[0].get("open", [])
        if hours_entries:
            hours_text = "; ".join([
                f"{entry.get('day', 'Mon')}: {entry.get('start', 'Closed')}-{entry.get('end', 'Closed')}"
                for entry in hours_entries
            ])
    
    # Attributes (accepts_credit_cards, parking_options, etc.)
    attributes = b.get("attributes", {}) or {}
    attributes_str = ", ".join([f"{k}: {v}" for k, v in attributes.items() if v]) if attributes else ""
    
    # Generate summary from attributes and reviews average
    summary = _generate_business_summary(name, category, price_range, attributes, rating, review_count)
    
    return {
        "name": name,
        "category": category,
        "description": description[:500],
        "address": address.strip() if address else "",
        "average_rating": rating,
        "total_reviews": review_count,
        "phone": phone,
        "website": website,
        "yelp_url": yelp_url,
        "latitude": latitude,
        "longitude": longitude,
        "price_range": price_range,
        "hours": hours_text[:500],
        "photo_url": photo_url,
        "attributes": attributes_str[:500],
        "summary": summary,
        "yelp_id": yelp_id
    }


def fetch_richmond_businesses(max_per_category=50):
    """
    Fetch businesses in Richmond, VA from Yelp across several categories.
    Returns list of dicts with name, category, description, address, average_rating, total_reviews.
    Returns [] if API key is missing or request fails. Use get_last_error() for failure reason.
    """
    global _last_error
    _last_error = None
    if not _get_api_key():
        _last_error = "YELP_API_KEY not set in config.py"
        return []
    all_businesses = {}
    searches = [
        ("restaurants", "Food"),
        ("shopping", "Retail"),
        ("localservices", "Services"),
        ("nightlife", "Entertainment"),
        ("gyms", "Health and Wellness"),
    ]
    for yelp_category, _app_category in searches:
        data, err = _request(limit=min(50, max_per_category), categories=yelp_category)
        if err:
            _last_error = err
            # Continue to next category; maybe one will work
            continue
        if not data or "businesses" not in data:
            continue
        for business_data in data.get("businesses", []):
            if business_data.get("is_closed"):
                continue
            row = _business_to_row(business_data)
            if not row:
                continue
            key = (row["name"].lower(), row["category"])
            if key not in all_businesses:
                all_businesses[key] = row
    return list(all_businesses.values())


def is_configured():
    """
    Check if the Yelp API is properly configured and ready to use.
    
    This verifies that a valid YELP_API_KEY is available (either from
    config.py or environment variable).
    
    Returns:
        bool: True if API key is set and non-empty, False otherwise
    """
    return bool(_get_api_key())
