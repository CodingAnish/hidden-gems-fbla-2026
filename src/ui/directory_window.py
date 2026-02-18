"""
Business Directory and Business Detail windows.
Hidden Gems | FBLA 2026
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import queries
from src.verification.verifier import get_challenge, verify_and_log
from src.ui.theme import apply_window_bg, COLORS, FONTS


def open_directory(parent, user):
    """Open the Business Directory as a Toplevel window."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Business Directory")
    top.geometry("640x520")
    apply_window_bg(top)
    _DirectoryFrame(top, user).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


class _DirectoryFrame(ttk.Frame):
    def __init__(self, parent, user, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.user = user
        self._businesses = []
        self._build()

    def _build(self):
        ttk.Label(self, text="Business Directory", style="Heading.TLabel").pack(anchor=tk.W, pady=(0, 4))
        ttk.Label(self, text="Filter, sort, and search Richmond businesses", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 12))
        row1 = ttk.Frame(self)
        row1.pack(fill=tk.X, pady=6)
        ttk.Label(row1, text="Category").pack(side=tk.LEFT, padx=(0, 8))
        self._cat_var = tk.StringVar(value="All")
        categories = ["All"] + queries.get_categories()
        self._cat_combo = ttk.Combobox(row1, textvariable=self._cat_var, values=categories, state="readonly", width=18)
        self._cat_combo.pack(side=tk.LEFT, padx=(0, 20))
        self._cat_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_list())
        ttk.Label(row1, text="Sort").pack(side=tk.LEFT, padx=(20, 8))
        self._sort_var = tk.StringVar(value="Name A–Z")
        self._sort_combo = ttk.Combobox(
            row1, textvariable=self._sort_var,
            values=["Name A–Z", "Highest rating", "Lowest rating", "Most reviews"],
            state="readonly", width=14
        )
        self._sort_combo.pack(side=tk.LEFT, padx=(0, 8))
        self._sort_combo.bind("<<ComboboxSelected>>", lambda e: self._refresh_list())
        ttk.Label(self, text="Search by name").pack(anchor=tk.W, pady=(10, 4))
        search_row = ttk.Frame(self)
        search_row.pack(fill=tk.X, pady=(0, 10))
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *a: self._refresh_list())
        self._search_entry = ttk.Entry(search_row, textvariable=self._search_var, width=32)
        self._search_entry.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(search_row, text="Search", command=self._refresh_list).pack(side=tk.LEFT)
        # List
        list_frame = ttk.Frame(self)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=8)
        columns = ("name", "category", "rating", "reviews", "deal")
        self._tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=14, selectmode="browse")
        self._tree.heading("name", text="Business")
        self._tree.heading("category", text="Category")
        self._tree.heading("rating", text="Rating")
        self._tree.heading("reviews", text="Reviews")
        self._tree.heading("deal", text="Deal")
        self._tree.column("name", width=200)
        self._tree.column("category", width=120)
        self._tree.column("rating", width=70)
        self._tree.column("reviews", width=70)
        self._tree.column("deal", width=50)
        scroll = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self._tree.yview)
        self._tree.configure(yscrollcommand=scroll.set)
        self._tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._tree.bind("<Double-1>", lambda e: self._view_details())
        self._empty_lbl = ttk.Label(self, text="", style="Caption.TLabel")
        self._empty_lbl.pack(anchor=tk.W, pady=6)
        btn_row = ttk.Frame(self)
        btn_row.pack(fill=tk.X, pady=12)
        ttk.Button(btn_row, text="View Details", command=self._view_details).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_row, text="Back", command=self.parent.destroy, style="Secondary.TButton").pack(side=tk.LEFT)
        self._refresh_list()

    def _get_sort_key(self):
        m = {"Name A–Z": "name", "Highest rating": "rating_high", "Lowest rating": "rating_low", "Most reviews": "reviews"}
        return m.get(self._sort_var.get(), "name")

    def _refresh_list(self):
        cat = self._cat_var.get()
        if cat == "All":
            cat = None
        sort_by = self._get_sort_key()
        search = (self._search_var.get() or "").strip()
        if search:
            self._businesses = queries.search_businesses_by_name(search)
            if cat:
                self._businesses = [b for b in self._businesses if b.get("category") == cat]
            if sort_by == "rating_high":
                self._businesses.sort(key=lambda b: (float(b.get("average_rating") or 0), (b.get("name") or "").lower()), reverse=True)
            elif sort_by == "rating_low":
                self._businesses.sort(key=lambda b: (float(b.get("average_rating") or 0), (b.get("name") or "").lower()))
            elif sort_by == "reviews":
                self._businesses.sort(key=lambda b: (int(b.get("total_reviews") or 0), (b.get("name") or "").lower()), reverse=True)
            else:
                self._businesses.sort(key=lambda b: (b.get("name") or "").lower())
        else:
            self._businesses = queries.get_businesses_for_directory(category=cat, sort_by=sort_by)
        ids_with_deals = queries.get_business_ids_with_deals()
        for i in self._tree.get_children():
            self._tree.delete(i)
        for b in self._businesses:
            bid = b.get("id")
            deal_tag = "Yes" if bid and bid in ids_with_deals else "—"
            self._tree.insert("", tk.END, values=(
                b.get("name") or "",
                b.get("category") or "",
                f"★ {b.get('average_rating') or 0}",
                b.get("total_reviews") or 0,
                deal_tag,
            ))
        if getattr(self, "_empty_lbl", None):
            self._empty_lbl.configure(
                text="No businesses match. Try a different filter or refresh from Yelp (Main Menu)." if not self._businesses else ""
            )

    def _view_details(self):
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("Select a business", "Select a business from the list, then click View Details or double-click.")
            return
        idx = self._tree.index(sel[0])
        if idx < 0 or idx >= len(self._businesses):
            return
        bid = self._businesses[idx].get("id")
        if bid:
            _open_business_detail(self.parent, self.user, bid)


def _open_business_detail(parent, user, business_id):
    """Open Business Detail as a Toplevel."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Business Details")
    top.geometry("540x560")
    apply_window_bg(top)
    _BusinessDetailFrame(top, user, business_id).pack(fill=tk.BOTH, expand=True, padx=20, pady=20)


def open_business_detail(parent, user, business_id):
    """Open Business Detail window (for use from Favorites, Recommendations, etc.)."""
    _open_business_detail(parent, user, business_id)


class _BusinessDetailFrame(ttk.Frame):
    def __init__(self, parent, user, business_id, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent
        self.user = user
        self.business_id = business_id
        self._business = queries.get_business_by_id(business_id)
        if not self._business:
            messagebox.showerror("Error", "Business not found.")
            parent.destroy()
            return
        self._build()

    def _build(self):
        b = self._business
        deals = queries.get_deals_by_business(self.business_id)
        title_row = ttk.Frame(self)
        title_row.pack(anchor=tk.W, pady=(0, 4))
        ttk.Label(title_row, text=b.get("name") or "Business", style="Heading.TLabel").pack(side=tk.LEFT)
        if deals:
            ttk.Label(title_row, text="  ·  Deal", style="Caption.TLabel").pack(side=tk.LEFT)
        ttk.Label(self, text=f"{b.get('category') or ''}  ·  ★ {b.get('average_rating') or 0}  ·  {b.get('total_reviews') or 0} reviews", style="Caption.TLabel").pack(anchor=tk.W, pady=(0, 10))
        ttk.Label(self, text="Address", style="Subheading.TLabel").pack(anchor=tk.W, pady=(6, 2))
        addr = (b.get("address") or "").strip()
        ttk.Label(self, text=addr if addr else "—", wraplength=480).pack(anchor=tk.W, pady=(0, 10))
        ttk.Separator(self, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=8)
        ttk.Label(self, text="Description", style="Subheading.TLabel").pack(anchor=tk.W, pady=(6, 2))
        desc = (b.get("description") or "No description.").strip()
        ttk.Label(self, text=desc, wraplength=480, justify=tk.LEFT).pack(anchor=tk.W, pady=(0, 10))
        if deals:
            ttk.Label(self, text="Deals", style="Subheading.TLabel").pack(anchor=tk.W, pady=(6, 2))
            for d in deals:
                ttk.Label(self, text=f"• {d.get('description') or ''}", wraplength=480).pack(anchor=tk.W, pady=2)
            ttk.Frame(self, height=10).pack()
        user_id = self.user.get("id")
        fav_ids = set(queries.get_favorite_business_ids(user_id)) if user_id else set()
        self._is_fav = self.business_id in fav_ids
        self._fav_btn = ttk.Button(
            self, text="Remove from Favorites" if self._is_fav else "Add to Favorites",
            command=self._toggle_favorite
        )
        self._fav_btn.pack(anchor=tk.W, pady=8)
        ttk.Label(self, text="Reviews", style="Subheading.TLabel").pack(anchor=tk.W, pady=(10, 4))
        rev_frame = ttk.Frame(self)
        rev_frame.pack(fill=tk.BOTH, expand=True, pady=4)
        scroll = ttk.Scrollbar(rev_frame)
        self._rev_text = tk.Text(
            rev_frame, height=8, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scroll.set,
            font=FONTS["body"], bg=COLORS["surface"], fg=COLORS["text"], insertbackground=COLORS["text"],
            padx=8, pady=8, relief="flat", borderwidth=0
        )
        scroll.config(command=self._rev_text.yview)
        self._rev_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self._fill_reviews()
        ttk.Button(self, text="Leave a Review", command=self._leave_review).pack(anchor=tk.W, pady=8)
        ttk.Button(self, text="Back", command=self.parent.destroy, style="Secondary.TButton").pack(anchor=tk.W, pady=6)

    def _fill_reviews(self):
        self._rev_text.config(state=tk.NORMAL)
        self._rev_text.delete("1.0", tk.END)
        reviews = queries.get_reviews_for_business(self.business_id)
        if not reviews:
            self._rev_text.insert(tk.END, "No reviews yet. Be the first to leave one!")
        else:
            for r in reviews:
                author = (r.get("username") or "").strip() or (r.get("email") or "").strip() or "User"
                self._rev_text.insert(tk.END, f"★ {r.get('rating')} — {author} ({r.get('created_date')} {r.get('created_time') or ''})\n")
                self._rev_text.insert(tk.END, f"  {r.get('review_text') or ''}\n\n")
        self._rev_text.config(state=tk.DISABLED)

    def _toggle_favorite(self):
        user_id = self.user.get("id")
        if not user_id:
            return
        # Verification before add (not before remove)
        if not self._is_fav:
            q, a = get_challenge()
            top = tk.Toplevel(self.parent)
            top.title("Verification")
            top.geometry("340x160")
            top.configure(bg=COLORS["bg"])
            ttk.Label(top, text=q).pack(pady=14, padx=16)
            ans_var = tk.StringVar()
            ttk.Entry(top, textvariable=ans_var, width=22).pack(pady=6, padx=16)
            def on_ok():
                user_ans = ans_var.get().strip()
                ok = verify_and_log(self.user.get("email") or "", user_ans, q, a, "favorite")
                top.destroy()
                if ok:
                    queries.add_favorite(user_id, self.business_id)
                    self._is_fav = True
                    self._fav_btn.config(text="Remove from Favorites")
                    messagebox.showinfo("Added", "Added to Favorites.")
                else:
                    messagebox.showerror("Verification failed", "Incorrect. Try again.")
            ttk.Button(top, text="Submit", command=on_ok, style="Primary.TButton").pack(pady=10)
            return
        queries.remove_favorite(user_id, self.business_id)
        self._is_fav = False
        self._fav_btn.config(text="Add to Favorites")
        messagebox.showinfo("Removed", "Removed from Favorites.")

    def _leave_review(self):
        user_id = self.user.get("id")
        if not user_id:
            return
        # Verification first
        q, a = get_challenge()
        top = tk.Toplevel(self.parent)
        top.title("Verification")
        top.geometry("360x180")
        top.configure(bg=COLORS["bg"])
        ttk.Label(top, text=q).pack(pady=12, padx=16)
        ans_var = tk.StringVar()
        ttk.Entry(top, textvariable=ans_var, width=24).pack(pady=6, padx=16)
        def on_verify():
            user_ans = ans_var.get().strip()
            ok = verify_and_log(self.user.get("email") or "", user_ans, q, a, "review")
            top.destroy()
            if ok:
                self._show_review_form()
            else:
                messagebox.showerror("Verification failed", "Incorrect. Try again.")
        ttk.Button(top, text="Continue", command=on_verify, style="Primary.TButton").pack(pady=10)
        return

    def _show_review_form(self):
        form = tk.Toplevel(self.parent)
        form.title("Leave a Review")
        form.geometry("420x280")
        form.configure(bg=COLORS["bg"])
        ttk.Label(form, text="Rating (1–5)").pack(anchor=tk.W, padx=16, pady=(14, 4))
        rating_var = tk.StringVar(value="5")
        ttk.Combobox(form, textvariable=rating_var, values=["1", "2", "3", "4", "5"], state="readonly", width=6).pack(anchor=tk.W, padx=16, pady=(0, 10))
        ttk.Label(form, text="Your review").pack(anchor=tk.W, padx=16, pady=(6, 4))
        text_w = tk.Text(form, height=6, width=48, wrap=tk.WORD, font=FONTS["body"], bg=COLORS["surface"], fg=COLORS["text"], padx=8, pady=8)
        text_w.pack(padx=16, pady=6, fill=tk.BOTH, expand=True)
        def submit():
            try:
                rating = int(rating_var.get())
            except (ValueError, TypeError):
                rating = 5
            if rating < 1 or rating > 5:
                rating = 5
            review_text = text_w.get("1.0", tk.END).strip()
            if not review_text:
                messagebox.showwarning("Missing text", "Please enter your review text.")
                return
            now = datetime.now()
            queries.add_review(self.business_id, self.user["id"], rating, review_text, now.strftime("%Y-%m-%d"), now.strftime("%H:%M"))
            form.destroy()
            self._fill_reviews()
            # Refresh business rating in case we're showing it
            self._business = queries.get_business_by_id(self.business_id)
            messagebox.showinfo("Thanks", "Your review was posted.")
        ttk.Button(form, text="Submit Review", command=submit, style="Primary.TButton").pack(pady=10)
        ttk.Button(form, text="Cancel", command=form.destroy, style="Secondary.TButton").pack(pady=(0, 14))
