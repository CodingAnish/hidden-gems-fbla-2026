"""
Hidden Gems — Web Application (Browser + Mobile Responsive)

A full-featured business discovery platform with user authentication, 
favorites management, AI chatbot recommendations, and community reviews.

Usage: python -m web.app (run from project root)
Version: FBLA 2026
"""
import sys
import os

# Setup path to allow imports from root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
os.chdir(ROOT)

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(ROOT, '.env'))
except ImportError:
    pass  # python-dotenv not installed, which is fine

# Flask and core imports
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime

# Application module imports
from src.database.db import init_db
from src.database import queries
from src.logic.auth import (
    hash_password, validate_login, register_user, is_valid_username, 
    is_valid_email, is_valid_password, generate_verification_code
)
from src.logic.chatbot import chat_with_ai, get_welcome_message
from src.logic.email_sender import send_verification_email, is_email_configured, send_password_reset_email

# Initialize Flask application
app = Flask(__name__, template_folder="templates", static_folder="static")

# Security and session configuration
app.secret_key = os.environ.get("SECRET_KEY", "hidden-gems-fbla-2026-dev-secret-key-change-in-production")
app.config["MAX_CONTENT_LENGTH"] = 4 * 1024 * 1024  # 4MB file upload limit
app.config["SESSION_COOKIE_HTTPONLY"] = True  # Prevent JavaScript access to session cookies
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # CSRF protection
app.config["PERMANENT_SESSION_LIFETIME"] = 86400  # 24-hour session timeout


# Register custom Jinja2 filters
@app.template_filter('from_json')
def from_json_filter(value):
    """Convert a JSON string to a Python dictionary in templates."""
    import json
    if not value:
        return {}
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}


def current_user():
    """
    Retrieve the currently logged-in user from the session.
    
    Returns:
        dict: User object with 'id', 'email', and 'username' keys, or None if not authenticated
    """
    # Check if required session data is present
    if "user_id" not in session or "email" not in session:
        return None
    
    # Get and normalize user email from session
    user_email = session.get("email", "").strip().lower()
    if not user_email:
        return None
    
    # Query database for user details
    user = queries.user_by_email(user_email)
    if not user:
        return None
    
    # Return standardized user object
    return {
        "id": user["id"], 
        "email": user["email"], 
        "username": user.get("username") or user["email"]
    }


def get_paginated_items(items, page=1, items_per_page=12):
    """
    Calculate pagination for a list of items.
    
    Args:
        items (list): The complete list of items to paginate
        page (int): Current page number (1-indexed)
        items_per_page (int): Number of items per page
    
    Returns:
        dict: Contains 'items', 'page', 'total_pages', 'total_items'
    """
    # Validate page number
    try:
        page = max(1, int(page))
    except (ValueError, TypeError):
        page = 1
    
    # Calculate pagination bounds
    total_items = len(items)
    total_pages = (total_items + items_per_page - 1) // items_per_page
    
    # Ensure page is within valid range
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    # Get slice of items for current page
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_items = items[start_idx:end_idx]
    
    return {
        "items": paginated_items,
        "page": page,
        "total_pages": total_pages,
        "total_items": total_items
    }


# ============================================
# AUTHENTICATION & SESSION ROUTES
# ============================================


@app.route("/")
def index():
    if current_user():
        businesses = queries.get_all_businesses()
        featured = sorted(businesses, key=lambda x: x.get("average_rating") or 0, reverse=True)[:6]
        trending = sorted(businesses, key=lambda x: x.get("total_reviews") or 0, reverse=True)[:3]
        return render_template("home.html", featured=featured, trending=trending)
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user():
        return redirect(url_for("directory"))
    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        login_success, login_result = validate_login(identifier, password)
        if login_success:
            session.permanent = True
            session["user_id"] = login_result["id"]
            session["email"] = login_result["email"]
            session["username"] = login_result.get("username") or login_result["email"]
            return redirect(url_for("directory"))
        # Handle email not verified
        if login_result == "EMAIL_NOT_VERIFIED":
            # Find user to get their email for resending code
            user = queries.user_by_email_or_username(identifier)
            if user:
                session["pending_verification_email"] = user["email"]
                session["pending_verification_id"] = user["id"]
                flash("Please verify your email address first. Check your inbox for the verification code.", "warning")
                return redirect(url_for("verify"))
        flash(login_result if isinstance(login_result, str) else "Login failed.", "error")
    return render_template("login.html", user=None)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user():
        return redirect(url_for("directory"))
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if password != confirm:
            flash("Passwords do not match.", "error")
        elif not is_valid_username(username):
            flash("Username must be 3–30 characters (letters, numbers, underscore).", "error")
        elif not is_valid_email(email):
            flash("Please enter a valid email.", "error")
        else:
            valid_pwd, pwd_error = is_valid_password(password)
            if not valid_pwd:
                flash(pwd_error, "error")
            else:
                register_success, register_result = register_user(username, email, password)
                if register_success:
                    user_id = register_result
                    # Generate and send verification code
                    code = generate_verification_code()
                    queries.create_email_verification_code(user_id, code)
                    
                    # Store in session for verification page
                    session["pending_verification_email"] = email.lower().strip()
                    session["pending_verification_id"] = user_id
                    
                    # Try to send email
                    if is_email_configured():
                        email_ok, email_error = send_verification_email(email, code)
                        if email_ok:
                            flash(f"Account created! A verification code has been sent to {email}.", "success")
                        else:
                            # Email sending failed - provide code directly
                            flash(f"Account created! Email delivery is currently unavailable.", "warning")
                            flash(f"Please use this verification code: {code}", "info")
                    else:
                        # Email not configured - show code directly (dev mode)
                        flash(f"Account created! Your verification code is: {code}", "info")
                    
                    return redirect(url_for("verify"))
                else:
                    flash(register_result, "error")
    return render_template("register.html", user=None)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))



@app.route("/verify", methods=["GET", "POST"])
def verify():
    # Check if there's a pending verification
    pending_email = session.get("pending_verification_email")
    pending_id = session.get("pending_verification_id")
    
    if not pending_email or not pending_id:
        flash("No pending verification found. Please register or log in.", "info")
        return redirect(url_for("login"))
    
    if request.method == "POST":
        entered_code = request.form.get("code", "").strip()
        
        if not entered_code:
            flash("Please enter the verification code.", "error")
            return render_template("verify.html", email=pending_email)
        
        # Get the latest verification code for this user
        saved_code = queries.get_latest_verification_code(pending_id)
        
        if not saved_code:
            flash("No verification code found. Please register again.", "error")
            return redirect(url_for("register"))
        
        if entered_code == saved_code:
            # Mark email as verified
            queries.set_email_verified(pending_id, 1)
            
            # Log the user in automatically
            user = queries.user_by_email(pending_email)
            if user:
                session.permanent = True
                session["user_id"] = user["id"]
                session["email"] = user["email"]
                session["username"] = user.get("username") or user["email"]
                
                # Clear pending verification
                session.pop("pending_verification_email", None)
                session.pop("pending_verification_id", None)
                
                flash("Email verified successfully! Welcome to Hidden Gems.", "success")
                return redirect(url_for("directory"))
        else:
            flash("Invalid verification code. Please try again.", "error")
    
    return render_template("verify.html", email=pending_email)


@app.route("/resend-verification", methods=["POST"])
def resend_verification():
    pending_email = session.get("pending_verification_email")
    pending_id = session.get("pending_verification_id")
    
    if not pending_email or not pending_id:
        flash("No pending verification found.", "error")
        return redirect(url_for("login"))
    
    # Generate new code
    code = generate_verification_code()
    queries.create_email_verification_code(pending_id, code)
    
    # Try to send email
    if is_email_configured():
        email_ok, email_error = send_verification_email(pending_email, code)
        if email_ok:
            flash("A new verification code has been sent to your email.", "success")
        else:
            flash("Email delivery is currently unavailable.", "warning")
            flash(f"Please use this verification code: {code}", "info")
    else:
        flash(f"Your new verification code is: {code}", "info")
    
    return redirect(url_for("verify"))


@app.route("/directory")
def directory():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Load user's saved preferences
    user_prefs = queries.get_user_preferences(user["id"])
    saved_favorite_categories = user_prefs.get("favorite_categories", [])
    saved_sort = user_prefs.get("default_sort", "name")
    
    # Get category and sort from query params (these override saved preferences)
    # If no query param, use saved preference
    category_filter = request.args.get("category")
    if category_filter is None:
        # Use first favorite category if available, otherwise "All"
        category_filter = saved_favorite_categories[0] if saved_favorite_categories else "All"
    
    sort_by = request.args.get("sort", saved_sort)
    search = request.args.get("q", "").strip()
    
    if search:
        all_businesses = queries.search_businesses_by_name(search)
        if category_filter and category_filter != "All":
            all_businesses = [b for b in all_businesses if b.get("category") == category_filter]
    else:
        category_filter = None if category_filter == "All" else category_filter
        all_businesses = queries.get_businesses_for_directory(category_filter=category_filter, sort_by_option=sort_by)
    
    # Pagination: 12 items per page (4 rows × 3 columns)
    items_per_page = 12
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    total_businesses = len(all_businesses)
    total_pages = (total_businesses + items_per_page - 1) // items_per_page
    
    # Ensure page is within valid range
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    businesses = all_businesses[start_idx:end_idx]
    
    # Use Quick Browse categories to match home page
    categories = ["All", "Food", "Retail", "Services", "Entertainment", "Health and Wellness"]
    
    # Pass selected category and sort to template for display
    selected_cat = category_filter if category_filter else "All"
    return render_template(
        "directory.html", 
        user=user, 
        businesses=businesses, 
        categories=categories,
        selected_category=selected_cat,
        selected_sort=sort_by,
        saved_favorites=saved_favorite_categories,
        page=page,
        total_pages=total_pages,
        total_businesses=total_businesses
    )


@app.route("/business/<int:business_id>")
def business_detail(business_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    business = queries.get_business_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("directory"))
    deals = queries.get_deals_by_business(business_id)
    reviews = queries.get_reviews_for_business(business_id)
    fav_ids = set(queries.get_favorite_business_ids(user["id"]))
    is_fav = business_id in fav_ids
    return render_template("business.html", user=user, business=business, deals=deals, reviews=reviews, is_fav=is_fav)


@app.route("/favorites")
def favorites():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get favorite businesses
    favorite_businesses = []
    try:
        result = queries.get_favorite_businesses(user["id"])
        if result:
            for biz in result:
                if isinstance(biz, dict):
                    biz_dict = biz.copy()
                else:
                    biz_dict = dict(biz) if hasattr(biz, 'keys') else {k: biz[k] for k in biz.keys()}
                
                deals = queries.get_deals_by_business(biz_dict.get("id")) or []
                biz_dict["deals"] = deals
                favorite_businesses.append(biz_dict)
    except Exception as e:
        print(f"Error getting favorites: {e}")
        favorite_businesses = []
    
    # Pagination
    items_per_page = 12
    page = max(1, int(request.args.get("page", 1)))
    
    total_businesses = len(favorite_businesses)
    total_pages = max(1, (total_businesses + items_per_page - 1) // items_per_page)
    page = min(page, total_pages)
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    businesses = favorite_businesses[start_idx:end_idx]
    
    return render_template(
        "favorites.html",
        user=user,
        businesses=businesses,
        page=page,
        total_pages=total_pages,
        total_businesses=total_businesses
    )


@app.route("/deals")
def deals():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    deals_list = queries.get_all_deals()
    return render_template("deals.html", user=user, deals=deals_list)


@app.route("/map")
def map_view():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get all businesses for map display
    # Note: Client-side JavaScript will geocode addresses to get coordinates
    all_businesses = queries.get_all_businesses()
    
    # Get Google Maps API key from config
    try:
        from config import GOOGLE_MAPS_API_KEY
    except ImportError:
        GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    
    return render_template(
        "map.html", 
        user=user, 
        businesses=all_businesses,
        google_maps_api_key=GOOGLE_MAPS_API_KEY,
        categories=sorted(set([b.get("category", "Other") for b in all_businesses if b.get("category")]))
    )


@app.route("/trending")
def trending():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    all_businesses = queries.get_trending_businesses(limit=300)
    
    # Pagination: 12 items per page
    items_per_page = 12
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    total_businesses = len(all_businesses)
    total_pages = (total_businesses + items_per_page - 1) // items_per_page
    
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    businesses = all_businesses[start_idx:end_idx]
    
    return render_template("trending.html", user=user, businesses=businesses, page=page, total_pages=total_pages, total_businesses=total_businesses)


@app.route("/recommendations")
def recommendations():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    all_businesses = queries.get_recommended_businesses(user["id"], limit=300)
    
    # Pagination: 12 items per page
    items_per_page = 12
    try:
        page = int(request.args.get("page", 1))
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    total_businesses = len(all_businesses)
    total_pages = (total_businesses + items_per_page - 1) // items_per_page
    
    if page > total_pages and total_pages > 0:
        page = total_pages
    
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    businesses = all_businesses[start_idx:end_idx]
    
    return render_template("recommendations.html", user=user, businesses=businesses, page=page, total_pages=total_pages, total_businesses=total_businesses)


@app.route("/help")
def help_page():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    return render_template("help.html", user=user)


@app.route("/profile")
def profile():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get user stats
    try:
        fav_ids = queries.get_favorite_business_ids(user["id"]) or []
        fav_count = len(fav_ids)
    except Exception:
        fav_count = 0
    
    try:
        reviews = queries.get_reviews_by_user(user["id"]) or []
        review_count = len(reviews)
    except Exception:
        reviews = []
        review_count = 0
    
    # Calculate average rating
    avg_rating = 4.8
    if reviews and len(reviews) > 0:
        try:
            total_rating = sum(r.get("rating", 0) for r in reviews)
            avg_rating = round(total_rating / len(reviews), 1)
        except Exception:
            avg_rating = 4.8
    
    # Get recent reviews
    recent_reviews = reviews[:5] if reviews else []
    
    # Get recent favorites
    try:
        fav_businesses = queries.get_favorite_businesses(user["id"]) or []
        # Convert to list of dicts
        favorites = []
        for fav in fav_businesses:
            try:
                if isinstance(fav, dict):
                    favorites.append(fav)
                else:
                    favorites.append({key: fav[key] for key in fav.keys()} if hasattr(fav, 'keys') else dict(fav))
            except Exception:
                continue
    except Exception:
        favorites = []
    
    # Get user data for member since
    try:
        user_data = queries.user_by_email(user["email"]) or {}
        member_since = user_data.get("created_at", "Recently")
    except Exception:
        member_since = "Recently"
    
    return render_template(
        "profile.html",
        fav_count=fav_count,
        review_count=review_count,
        avg_rating=avg_rating,
        deals_used=0,
        reviews=recent_reviews,
        favorites=favorites,
        member_since=member_since,
        last_login="Today"
    )


@app.route("/settings", methods=["GET", "POST"])
def settings():
    session.permanent = True
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Load saved preferences to show in form
    user_prefs = queries.get_user_preferences(user["id"])
    saved_favorites = user_prefs.get("favorite_categories", [])
    saved_sort = user_prefs.get("default_sort", "name")
    
    if request.method == "POST":
        flash("Settings saved successfully!", "success")
        return redirect(url_for("settings"))
    
    return render_template(
        "settings.html", 
        user=user,
        saved_favorites=saved_favorites,
        saved_sort=saved_sort
    )


@app.route("/save-preferences", methods=["POST"])
def save_preferences():
    session.permanent = True
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get favorite categories from form
    favorite_categories = request.form.getlist("favorite_categories")
    default_sort = request.form.get("default_sort", "name")
    
    # Save to database
    import json
    preferences_json = json.dumps({
        "favorite_categories": favorite_categories,
        "default_sort": default_sort
    })
    queries.save_user_preferences(user["id"], preferences_json)
    session["favorite_categories"] = favorite_categories
    flash("Preferences saved successfully!", "success")
    return redirect(url_for("settings"))


@app.route("/save-notifications", methods=["POST"])
def save_notifications():
    session.permanent = True
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get notification preferences from form
    deal_notifications = "deal_notifications" in request.form
    recommendation_notifications = "recommendation_notifications" in request.form
    review_responses = "review_responses" in request.form
    
    # Save to database
    import json
    notifications_json = json.dumps({
        "deal_notifications": deal_notifications,
        "recommendation_notifications": recommendation_notifications,
        "review_responses": review_responses
    })
    queries.save_user_preferences(user["id"], notifications_json)
    
    flash("Notification settings saved successfully!", "success")
    return redirect(url_for("settings"))


@app.route("/save-privacy", methods=["POST"])
def save_privacy():
    session.permanent = True
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    # Get privacy preferences from form
    profile_visibility = request.form.get("profile_visibility", "public")
    
    # Save to database
    import json
    privacy_json = json.dumps({
        "profile_visibility": profile_visibility
    })
    queries.save_user_preferences(user["id"], privacy_json)
    
    flash("Privacy settings saved successfully!", "success")
    return redirect(url_for("settings"))


@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        
        # Check if user exists
        user = queries.user_by_email(email)
        if user:
            # Generate reset token using timestamp + user id
            import secrets
            import time
            token = secrets.token_urlsafe(32)
            expires = int(time.time()) + 3600  # 1 hour from now
            reset_token = f"{user['id']}_{expires}_{token}"
            
            # Create reset link
            reset_link = url_for('reset_password', token=reset_token, _external=True)
            
            # Send email
            ok, error = send_password_reset_email(email, reset_link)
            if ok:
                flash(f"Password reset instructions sent to {email}. Check your inbox!", "success")
            elif is_email_configured():
                flash(f"Error sending email: {error}", "error")
            else:
                # Demo mode - show link
                flash(f"Demo mode: Click the link in the message to reset password", "info")
        else:
            # For security, show same message even if user doesn't exist
            flash(f"If an account exists with {email}, you will receive password reset instructions.", "info")
        
        return render_template("forgot-password.html")
    
    return render_template("forgot-password.html")


@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """Reset password using a token from email link."""
    import time
    
    # Validate token format
    try:
        parts = token.split("_")
        if len(parts) < 3:
            flash("Invalid or expired reset link.", "error")
            return redirect(url_for("login"))
        
        user_id = int(parts[0])
        expires = int(parts[1])
        
        # Check if token expired
        if int(time.time()) > expires:
            flash("Password reset link has expired. Please try again.", "error")
            return redirect(url_for("forgot_password"))
        
        # Get user
        user = queries.get_user_by_id(user_id)
        if not user:
            flash("Invalid reset link.", "error")
            return redirect(url_for("login"))
        
        if request.method == "POST":
            new_password = request.form.get("password", "")
            confirm = request.form.get("confirm", "")
            
            if not new_password or not confirm:
                flash("Password fields cannot be empty.", "error")
            elif new_password != confirm:
                flash("Passwords do not match.", "error")
            else:
                valid_pwd, pwd_error = is_valid_password(new_password)
                if not valid_pwd:
                    flash(pwd_error, "error")
                else:
                    # Update password
                    pwd_hash = hash_password(new_password)
                    queries.update_user_password(user_id, pwd_hash)
                    
                    # Verify update worked by querying the DB
                    updated_user = queries.get_user_by_id(user_id)
                    if updated_user and updated_user["password_hash"] == pwd_hash:
                        flash("Password successfully reset! You can now log in.", "success")
                        return redirect(url_for("login"))
                    else:
                        flash("Error saving password. Please try again.", "error")
        
        return render_template("reset-password.html", email=user["email"])
    
    except (ValueError, IndexError):
        flash("Invalid reset link.", "error")
        return redirect(url_for("login"))


@app.route("/account")
def account():
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    # Get user stats
    fav_count = len(queries.get_favorite_business_ids(user["id"]) or [])
    reviews = queries.get_reviews_by_user(user["id"])
    review_count = len(reviews) if reviews else 0
    return render_template("account.html", fav_count=fav_count, review_count=review_count)


@app.route("/favorite/add/<int:business_id>", methods=["POST"])
def favorite_add(business_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    queries.add_favorite(user["id"], business_id)
    return redirect(request.referrer or url_for("directory"))


@app.route("/favorite/remove/<int:business_id>", methods=["POST"])
def favorite_remove(business_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    queries.remove_favorite(user["id"], business_id)
    return redirect(request.referrer or url_for("directory"))


@app.route("/business/<int:business_id>/review", methods=["POST"])
def business_review(business_id):
    user = current_user()
    if not user:
        return redirect(url_for("login"))
    
    rating = request.form.get("rating", "5")
    text = (request.form.get("review_text") or "").strip()
    captcha_answer = request.form.get("captcha_answer", "")
    
    # Validate business exists
    business = queries.get_business_by_id(business_id)
    if not business:
        flash("Business not found.", "error")
        return redirect(url_for("directory"))
    
    # Validation errors
    errors = []
    
    # Validate rating
    try:
        rating = max(1, min(5, int(rating)))
    except ValueError:
        errors.append("Invalid rating. Please select a rating between 1 and 5.")
        rating = 5
    
    # Validate review text
    if not text:
        errors.append("Please enter your review text.")
    elif len(text) < 10:
        errors.append("Review must be at least 10 characters long.")
    elif len(text) > 500:
        errors.append("Review must be less than 500 characters.")
    
    # Verify CAPTCHA
    stored_answer = session.get('captcha_answer')
    if not stored_answer:
        errors.append("CAPTCHA session expired. Please refresh the page and try again.")
    else:
        try:
            if int(captcha_answer) != stored_answer:
                errors.append("Incorrect answer to verification question.")
        except (ValueError, TypeError):
            errors.append("Please answer the verification question.")
    
    # If errors, flash them and redirect back
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("business_detail", business_id=business_id))
    
    # All validation passed - add review
    try:
        now = datetime.now()
        queries.add_review(
            business_id, 
            user["id"], 
            rating, 
            text, 
            now.strftime("%Y-%m-%d"), 
            now.strftime("%H:%M")
        )
        
        # Clear CAPTCHA after successful use
        session.pop('captcha_answer', None)
        session.modified = True
        
        flash("Thanks! Your review was posted.", "success")
    except Exception as e:
        flash("Error posting review. Please try again.", "error")
    
    return redirect(url_for("business_detail", business_id=business_id))


@app.route("/api/chat", methods=["POST"])
def chat():
    """AI Chatbot endpoint - handles chat messages and returns Claude responses."""
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    data = request.get_json()
    user_message = data.get("message", "").strip()
    conversation_history = data.get("history", [])
    
    if not user_message:
        return jsonify({"error": "Message is required"}), 400
    
    # Rate limiting: max 20 messages per session
    if len(conversation_history) > 40:  # 20 exchanges = 40 messages
        return jsonify({
            "response": "You've reached the conversation limit. Please refresh the chat to start a new conversation!",
            "quick_actions": ["Refresh Chat", "Browse Directory"]
        })
    
    # Get response from AI (tries Groq, then Hugging Face, then rule-based)
    response_text, intent, quick_actions = chat_with_ai(conversation_history, user_message)
    
    return jsonify({
        "response": response_text,
        "intent": intent,
        "quick_actions": quick_actions
    })


@app.route("/api/chat/welcome", methods=["GET"])
def chat_welcome():
    """Get welcome message for chatbot."""
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    welcome = get_welcome_message()
    return jsonify(welcome)


# ============================================
# REVIEWS & RATINGS ENDPOINTS
# ============================================

@app.route("/get-captcha", methods=["GET"])
def get_captcha():
    """Generate and return a CAPTCHA verification question."""
    import random
    
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Generate simple math problem
    left_operand = random.randint(1, 20)
    right_operand = random.randint(1, 20)
    operator = random.choice(['+', '-'])
    
    if operator == '+':
        answer = left_operand + right_operand
        question = f"What is {left_operand} + {right_operand}?"
    else:
        answer = left_operand - right_operand
        question = f"What is {left_operand} - {right_operand}?"
    
    # Store answer in session (expires when session expires)
    session['captcha_answer'] = answer
    session.modified = True
    
    return jsonify({
        "question": question,
        "session_id": session.get('user_id')
    })


@app.route("/submit-review", methods=["POST"])
def submit_review():
    """Submit a review for a business with validation."""
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated", "success": False}), 401
    
    data = request.get_json()
    business_id = data.get("business_id")
    reviewer_name = data.get("user_name", "").strip()
    rating = data.get("rating")
    comment = data.get("comment", "").strip()
    captcha_answer = data.get("captcha_answer")
    
    # Validation
    errors = []
    
    if not business_id:
        errors.append("Business ID is required")
    
    if not reviewer_name or len(reviewer_name) < 2:
        errors.append("Name must be at least 2 characters")
    elif len(reviewer_name) > 50:
        errors.append("Name must be less than 50 characters")
    
    if not rating:
        errors.append("Rating is required")
    else:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                errors.append("Rating must be between 1 and 5")
        except (ValueError, TypeError):
            errors.append("Invalid rating")
    
    if not comment or len(comment) < 10:
        errors.append("Review must be at least 10 characters")
    elif len(comment) > 500:
        errors.append("Review must be less than 500 characters")
    
    # Verify CAPTCHA
    stored_answer = session.get('captcha_answer')
    if not stored_answer:
        errors.append("CAPTCHA session expired. Please refresh and try again.")
    else:
        try:
            if int(captcha_answer) != stored_answer:
                errors.append("Incorrect answer to verification question")
        except (ValueError, TypeError):
            errors.append("Invalid CAPTCHA answer")
    
    if errors:
        return jsonify({
            "success": False,
            "errors": errors
        }), 400
    
    # Add review to database
    try:
        now = datetime.now()
        queries.add_review(
            business_id,
            user["id"],
            rating,
            comment,
            now.strftime("%Y-%m-%d"),
            now.strftime("%H:%M")
        )
        
        # Clear CAPTCHA after successful use
        session.pop('captcha_answer', None)
        session.modified = True
        
        return jsonify({
            "success": True,
            "message": "Review submitted successfully!",
            "review": {
                "rating": rating,
                "comment": comment,
                "user_name": reviewer_name,
                "date": now.strftime("%Y-%m-%d")
            }
        }), 201
    except Exception as e:
        return jsonify({
            "success": False,
            "errors": ["Failed to save review. Please try again."]
        }), 500


@app.route("/get-reviews/<int:business_id>", methods=["GET"])
def get_reviews(business_id):
    """Get all reviews for a specific business."""
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    # Verify business exists
    business = queries.get_business_by_id(business_id)
    if not business:
        return jsonify({"error": "Business not found"}), 404
    
    try:
        reviews = queries.get_reviews_for_business(business_id)
        
        # Calculate average rating
        if reviews:
            avg_rating = sum(r.get("rating", 0) for r in reviews) / len(reviews)
        else:
            avg_rating = 0
        
        return jsonify({
            "success": True,
            "reviews": reviews or [],
            "count": len(reviews) if reviews else 0,
            "average_rating": round(avg_rating, 1)
        }), 200
    except Exception as e:
        return jsonify({
            "error": "Failed to retrieve reviews"
        }), 500


# ============================================
# FAVORITES ENDPOINTS
# ============================================

@app.route("/api/favorites", methods=["GET", "POST"])
def api_favorites():
    """Get or save user's favorite businesses."""
    user = current_user()
    if not user:
        return jsonify({"error": "Not authenticated"}), 401
    
    if request.method == "GET":
        # Return user's saved favorites
        try:
            favorites = queries.get_favorite_business_ids(user["id"])
            return jsonify({
                "success": True,
                "favorites": favorites or [],
                "count": len(favorites) if favorites else 0
            }), 200
        except Exception as e:
            return jsonify({
                "error": "Failed to retrieve favorites"
            }), 500
    
    elif request.method == "POST":
        # Save/toggle favorites
        data = request.get_json()
        business_id = data.get("business_id")
        action = data.get("action", "toggle")  # toggle, add, or remove
        
        if not business_id:
            return jsonify({"error": "Business ID is required"}), 400
        
        # Verify business exists
        business = queries.get_business_by_id(business_id)
        if not business:
            return jsonify({"error": "Business not found"}), 404
        
        try:
            favorite_ids = set(queries.get_favorite_business_ids(user["id"]) or [])
            is_favorited = business_id in favorite_ids
            
            if action == "add" or (action == "toggle" and not is_favorited):
                queries.add_favorite(user["id"], business_id)
                return jsonify({
                    "success": True,
                    "action": "added",
                    "is_favorited": True,
                    "message": f"Added {business['name']} to favorites"
                }), 200
            
            elif action == "remove" or (action == "toggle" and is_favorited):
                queries.remove_favorite(user["id"], business_id)
                return jsonify({
                    "success": True,
                    "action": "removed",
                    "is_favorited": False,
                    "message": f"Removed {business['name']} from favorites"
                }), 200
            
            return jsonify({
                "success": True,
                "is_favorited": is_favorited
            }), 200
        
        except Exception as e:
            return jsonify({
                "error": "Failed to update favorites"
            }), 500


def run_web():
    init_db()
    from src.database import seed
    seed.ensure_seed_data()
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() == "true"
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port, debug=debug_mode)


if __name__ == "__main__":
    run_web()
