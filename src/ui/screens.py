"""
Favorites, Deals, Help, and Recommendations screens.
Hidden Gems | FBLA 2026
"""
import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import queries
from src.ui.directory_window import open_business_detail
from src.ui.theme import apply_window_bg, COLORS, FONTS


def open_favorites(parent, user):
    """Open Favorites list window."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Favorites")
    top.geometry("580x440")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="Your Favorite Businesses", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
    ttk.Label(f, text="Businesses you've saved — double-click to open", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
    user_id = user.get("id")
    businesses = queries.get_favorite_businesses(user_id) if user_id else []
    if not businesses:
        ttk.Label(f, text="You have no favorites yet. Add some from the Business Directory!", style="Caption.TLabel").pack(anchor=tk.W, pady=12)
        ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=10)
        return
    tree_frame = ttk.Frame(f)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    cols = ("name", "category", "rating", "reviews")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12, selectmode="browse")
    tree.heading("name", text="Business")
    tree.heading("category", text="Category")
    tree.heading("rating", text="Rating")
    tree.heading("reviews", text="Reviews")
    tree.column("name", width=220)
    tree.column("category", width=140)
    tree.column("rating", width=80)
    tree.column("reviews", width=80)
    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    for b in businesses:
        tree.insert("", tk.END, values=(
            b.get("name") or "",
            b.get("category") or "",
            f"★ {b.get('average_rating') or 0}",
            b.get("total_reviews") or 0,
        ))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def view_details():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select one", "Select a business, then click View Details.")
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(businesses):
            open_business_detail(top, user, businesses[idx]["id"])

    def remove_fav():
        sel = tree.selection()
        if not sel:
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(businesses):
            bid = businesses[idx]["id"]
            queries.remove_favorite(user_id, bid)
            businesses.pop(idx)
            tree.delete(sel[0])
            messagebox.showinfo("Removed", "Removed from favorites.")

    tree.bind("<Double-1>", lambda e: view_details())
    btn_row = ttk.Frame(f)
    btn_row.pack(fill=tk.X, pady=12)
    ttk.Button(btn_row, text="View Details", command=view_details).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Remove from Favorites", command=remove_fav, style="Secondary.TButton").pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Back", command=top.destroy, style="Secondary.TButton").pack(side=tk.LEFT)


def open_deals(parent, user=None):
    """Open All Deals window. user needed for View business -> detail."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Deals")
    top.geometry("620x460")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="All Deals & Coupons", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
    ttk.Label(f, text="Select a deal and click View Business to see full details.", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
    deals = queries.get_all_deals()
    if not deals:
        ttk.Label(f, text="No deals available right now. Check back later!", style="Caption.TLabel").pack(anchor=tk.W, pady=12)
        ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=10)
        return
    tree_frame = ttk.Frame(f)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    cols = ("business_name", "description")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14, selectmode="browse")
    tree.heading("business_name", text="Business")
    tree.heading("description", text="Deal")
    tree.column("business_name", width=200)
    tree.column("description", width=360)
    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    for d in deals:
        tree.insert("", tk.END, values=(d.get("business_name") or "", d.get("description") or ""))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def view_business():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select a deal", "Select a deal, then click View Business.")
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(deals) and user:
            open_business_detail(top, user, deals[idx].get("business_id"))

    tree.bind("<Double-1>", lambda e: view_business())
    btn_row = ttk.Frame(f)
    btn_row.pack(fill=tk.X, pady=12)
    if user:
        ttk.Button(btn_row, text="View Business", command=view_business).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Back", command=top.destroy, style="Secondary.TButton").pack(side=tk.LEFT)


def open_help(parent):
    """Open Help / Instructions window."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Help")
    top.geometry("520x500")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="How to Use Hidden Gems", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 8))
    text = tk.Text(f, wrap=tk.WORD, font=FONTS["body"], height=22, padx=12, pady=12, bg=COLORS["surface"], fg=COLORS["text"], relief="flat")
    text.pack(fill=tk.BOTH, expand=True)
    help_content = """
Hidden Gems helps you discover and support small local businesses in the Richmond, VA area.

MAIN MENU — BROWSE
• Business Directory — Browse all businesses. Filter by category, sort by rating or name, search by name. The "Deal" column shows which businesses have current deals. Double-click or click View Details to open a business.
• Trending — See popular businesses (top rated and most reviewed).
• Recommendations — Personalized picks based on your favorites and popular Richmond businesses.
• Deals — View all current deals and coupons. Click View Business to open that business's page.

YOUR ACCOUNT
• Favorites — Businesses you've bookmarked. Add from a business detail page (verification required).
• My Reviews — See all reviews you've written and jump to the business.

BUSINESS DETAILS
• View address, description, rating, and review count.
• See deals for that business.
• Add or remove from Favorites (adding requires a quick verification).
• Read reviews and leave your own (verification required). Reviews show usernames when set.

VERIFICATION
Before leaving a review or adding a favorite, you'll complete a short verification (e.g. a simple math question or code) to prevent automated abuse. Every attempt is recorded in the Verification Table.

DATA
All data is stored locally in the SQLite database (hidden_gems.db). Businesses can be loaded from the Yelp API for Richmond, VA when an API key is set in config.py.
"""
    text.insert(tk.END, help_content.strip())
    text.config(state=tk.DISABLED)
    ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=12)


def open_recommendations(parent, user):
    """Open Recommendations window (intelligent feature)."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Recommendations")
    top.geometry("620x460")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="Recommended for You", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
    ttk.Label(f, text="Based on your favorites and popular Richmond businesses", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
    user_id = user.get("id")
    businesses = queries.get_recommended_businesses(user_id, limit=25) if user_id else []
    if not businesses:
        ttk.Label(f, text="Add some favorites first to get personalized recommendations, or browse the Business Directory.", style="Caption.TLabel").pack(anchor=tk.W, pady=12)
        ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=10)
        return
    tree_frame = ttk.Frame(f)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    cols = ("name", "category", "rating", "reviews")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14, selectmode="browse")
    tree.heading("name", text="Business")
    tree.heading("category", text="Category")
    tree.heading("rating", text="Rating")
    tree.heading("reviews", text="Reviews")
    tree.column("name", width=220)
    tree.column("category", width=140)
    tree.column("rating", width=80)
    tree.column("reviews", width=80)
    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    for b in businesses:
        tree.insert("", tk.END, values=(
            b.get("name") or "",
            b.get("category") or "",
            f"★ {b.get('average_rating') or 0}",
            b.get("total_reviews") or 0,
        ))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def view_details():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select one", "Select a business, then click View Details.")
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(businesses):
            open_business_detail(top, user, businesses[idx]["id"])

    tree.bind("<Double-1>", lambda e: view_details())
    btn_row = ttk.Frame(f)
    btn_row.pack(fill=tk.X, pady=12)
    ttk.Button(btn_row, text="View Details", command=view_details).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Back", command=top.destroy, style="Secondary.TButton").pack(side=tk.LEFT)


def open_trending(parent, user):
    """Open Trending / Most Popular businesses window."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Trending")
    top.geometry("620x460")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="Trending & Popular", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
    ttk.Label(f, text="Top-rated and most-reviewed businesses in Richmond", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
    businesses = queries.get_trending_businesses(limit=30)
    if not businesses:
        ttk.Label(f, text="No businesses in the directory yet. Refresh from Yelp or add seed data.", style="Caption.TLabel").pack(anchor=tk.W, pady=12)
        ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=10)
        return
    tree_frame = ttk.Frame(f)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    cols = ("name", "category", "rating", "reviews")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=14, selectmode="browse")
    tree.heading("name", text="Business")
    tree.heading("category", text="Category")
    tree.heading("rating", text="Rating")
    tree.heading("reviews", text="Reviews")
    tree.column("name", width=220)
    tree.column("category", width=140)
    tree.column("rating", width=80)
    tree.column("reviews", width=80)
    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    for b in businesses:
        tree.insert("", tk.END, values=(
            b.get("name") or "",
            b.get("category") or "",
            f"★ {b.get('average_rating') or 0}",
            b.get("total_reviews") or 0,
        ))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def view_details():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select one", "Select a business, then click View Details.")
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(businesses):
            open_business_detail(top, user, businesses[idx]["id"])

    tree.bind("<Double-1>", lambda e: view_details())
    btn_row = ttk.Frame(f)
    btn_row.pack(fill=tk.X, pady=12)
    ttk.Button(btn_row, text="View Details", command=view_details).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Back", command=top.destroy, style="Secondary.TButton").pack(side=tk.LEFT)


def open_my_reviews(parent, user):
    """Open My Reviews window — list of reviews written by the user."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — My Reviews")
    top.geometry("640x480")
    apply_window_bg(top)
    f = ttk.Frame(top, padding=20)
    f.pack(fill=tk.BOTH, expand=True)
    ttk.Label(f, text="My Reviews", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
    ttk.Label(f, text="Reviews you've written — click View Business to open the business page.", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
    user_id = user.get("id")
    reviews = queries.get_reviews_by_user(user_id) if user_id else []
    if not reviews:
        ttk.Label(f, text="You haven't written any reviews yet. Visit a business and click Leave a Review!", style="Caption.TLabel").pack(anchor=tk.W, pady=12)
        ttk.Button(f, text="Back", command=top.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=10)
        return
    tree_frame = ttk.Frame(f)
    tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    cols = ("business_name", "rating", "date", "snippet")
    tree = ttk.Treeview(tree_frame, columns=cols, show="headings", height=12, selectmode="browse")
    tree.heading("business_name", text="Business")
    tree.heading("rating", text="Rating")
    tree.heading("date", text="Date")
    tree.heading("snippet", text="Review")
    tree.column("business_name", width=180)
    tree.column("rating", width=60)
    tree.column("date", width=100)
    tree.column("snippet", width=280)
    scroll = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    for r in reviews:
        text = (r.get("review_text") or "").strip()
        snippet = (text[:60] + "…") if len(text) > 60 else text
        date_str = f"{r.get('created_date') or ''} {r.get('created_time') or ''}".strip()
        tree.insert("", tk.END, values=(
            r.get("business_name") or "",
            f"★ {r.get('rating')}",
            date_str,
            snippet or "—",
        ))
    tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scroll.pack(side=tk.RIGHT, fill=tk.Y)

    def view_business():
        sel = tree.selection()
        if not sel:
            messagebox.showinfo("Select one", "Select a review, then click View Business.")
            return
        idx = tree.index(sel[0])
        if 0 <= idx < len(reviews):
            open_business_detail(top, user, reviews[idx].get("business_id"))

    tree.bind("<Double-1>", lambda e: view_business())
    btn_row = ttk.Frame(f)
    btn_row.pack(fill=tk.X, pady=12)
    ttk.Button(btn_row, text="View Business", command=view_business).pack(side=tk.LEFT, padx=(0, 10))
    ttk.Button(btn_row, text="Back", command=top.destroy, style="Secondary.TButton").pack(side=tk.LEFT)
