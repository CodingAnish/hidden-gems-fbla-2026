"""
Main menu — Complete, polished mobile-app UI with fully populated pages.
Hidden Gems | FBLA 2026
"""
import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import queries
from src.logic.yelp_api import is_configured as yelp_configured
from src.database.seed import refresh_richmond_from_yelp, replace_all_with_yelp
from src.ui.directory_window import open_directory
from src.ui.screens import open_favorites, open_deals, open_help, open_recommendations, open_trending, open_my_reviews
from src.ui.account_settings import open_account_settings
from src.logic.yelp_api import get_last_error
from src.ui.theme import apply_window_bg
from src.ui.design_system import COLORS, FONTS, LAYOUT, SPACING
from src.ui.components import (
    TopNavBar, BottomNavBar, HeroSection, PremiumCard, 
    FeaturedCard, ToastNotification, EnhancedEntry
)
from src.state import set_user, get_user


class MainMenuWindow:
    def __init__(self, user):
        set_user(user)
        self.user = user
        self.current_view = "home"
        self.win = tk.Tk()
        self.win.title("Hidden Gems")
        self.win.geometry("750x860+50+50")
        self.win.minsize(700, 820)
        self.win.resizable(True, True)
        apply_window_bg(self.win)
        self._build()
        self._bring_to_front()
        
        # Show welcome toast
        self.win.after(500, lambda: ToastNotification.show(
            self.win, 
            f"Welcome back, {user.get('username', 'User')}!",
            "success"
        ))

    def _bring_to_front(self):
        """Force window on-screen and to the front."""
        self.win.update_idletasks()
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.after(200, lambda: self.win.attributes("-topmost", False))
        self.win.focus_force()

    def _build(self):
        # Top navigation
        TopNavBar(self.win, user=self.user, on_profile_click=self._show_profile_view)
        
        # Main content area with canvas for scrolling
        self.main_frame = tk.Frame(self.win, bg=COLORS["bg"])
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.main_frame, bg=COLORS["bg"], highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self.main_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=COLORS["bg"])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        
        # Enable mousewheel scrolling
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Content container
        self.content_container = self.scrollable_frame
        
        # Bottom navigation
        BottomNavBar(self.win, active=self.current_view, on_nav_click=self._handle_nav_click)
        
        # Build initial view
        self._build_home_view()
    
    def _handle_nav_click(self, tab_id):
        """Handle bottom navigation clicks."""
        self.current_view = tab_id
        
        # Clear content
        for widget in self.content_container.winfo_children():
            widget.destroy()
        
        # Reset scroll
        self.canvas.yview_moveto(0)
        
        # Build appropriate view
        if tab_id == "home":
            self._build_home_view()
        elif tab_id == "browse":
            self._build_browse_view()
        elif tab_id == "favorites":
            self._build_favorites_view()
        elif tab_id == "profile":
            self._build_profile_view()
    
    def _show_profile_view(self):
        """Show profile view when avatar clicked."""
        self._handle_nav_click("profile")
    
    def _ensure_businesses_loaded(self):
        """Check if businesses exist, if not, try to load from Yelp."""
        all_businesses = queries.get_all_businesses()
        if not all_businesses and yelp_configured():
            # Try to load from Yelp
            from src.database.seed import refresh_richmond_from_yelp
            added, updated = refresh_richmond_from_yelp()
            if added > 0:
                ToastNotification.show(self.win, f"Loaded {added} businesses from Yelp!", "success")
            elif get_last_error():
                ToastNotification.show(self.win, f"Yelp API error: {get_last_error()}", "error")
    
    def _build_home_view(self):
        """Complete home view with hero, stats, featured, trending, and quick actions."""
        # Ensure businesses are loaded
        self._ensure_businesses_loaded()
        
        container = tk.Frame(self.content_container, bg=COLORS["bg"])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Welcome hero card
        hero_card = tk.Frame(container, bg=COLORS["primary"], highlightthickness=0)
        hero_card.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        
        hero_content = tk.Frame(hero_card, bg=COLORS["primary"])
        hero_content.pack(fill=tk.X, padx=SPACING["xl"], pady=SPACING["xl"])
        
        username = self.user.get("username", "User")
        tk.Label(
            hero_content,
            text=f"Welcome back, {username}! 👋",
            font=FONTS["hero"],
            fg=COLORS["surface"],
            bg=COLORS["primary"],
        ).pack(anchor=tk.W, pady=(0, SPACING["sm"]))
        
        tk.Label(
            hero_content,
            text="Discover and support Richmond's local businesses",
            font=FONTS["body_large"],
            fg=COLORS["primary_light"],
            bg=COLORS["primary"],
        ).pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        
        # Search bar in hero
        search_frame = tk.Frame(hero_content, bg=COLORS["surface"], highlightthickness=0)
        search_frame.pack(fill=tk.X)
        
        search_entry = tk.Entry(
            search_frame,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=FONTS["body"],
            relief=tk.FLAT,
            borderwidth=0,
        )
        search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
        search_entry.insert(0, "Search businesses...")
        search_entry.config(fg=COLORS["text_muted"])
        
        def on_search_focus(e):
            if search_entry.get() == "Search businesses...":
                search_entry.delete(0, tk.END)
                search_entry.config(fg=COLORS["text"])
        
        search_entry.bind("<FocusIn>", on_search_focus)
        
        tk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI Emoji", 16),
            bg=COLORS["surface"],
            cursor="hand2"
        ).pack(side=tk.RIGHT, padx=SPACING["md"])
        
        # Main content
        content = tk.Frame(container, bg=COLORS["bg"], padx=SPACING["xl"])
        content.pack(fill=tk.BOTH, expand=True)
        
        # Quick stats
        stats_row = tk.Frame(content, bg=COLORS["bg"])
        stats_row.pack(fill=tk.X, pady=(SPACING["lg"], SPACING["xl"]))
        
        user_stats = queries.get_user_stats(self.user.get("id"))
        
        stats_data = [
            {"icon": "📝", "value": str(user_stats["review_count"]), "label": "Reviews"},
            {"icon": "❤️", "value": str(user_stats["favorite_count"]), "label": "Favorites"},
            {"icon": "⭐", "value": str(user_stats["avg_rating_given"]), "label": "Avg Rating"},
        ]
        
        for i, stat in enumerate(stats_data):
            stat_card = tk.Frame(stats_row, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, SPACING["sm"] if i < 2 else 0))
            
            stat_content = tk.Frame(stat_card, bg=COLORS["surface"])
            stat_content.pack(fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["lg"])
            
            tk.Label(
                stat_content,
                text=stat["icon"],
                font=("Segoe UI Emoji", 28),
                bg=COLORS["surface"],
            ).pack()
            
            tk.Label(
                stat_content,
                text=stat["value"],
                font=FONTS["heading"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack(pady=(SPACING["xs"], 0))
            
            tk.Label(
                stat_content,
                text=stat["label"],
                font=FONTS["caption"],
                fg=COLORS["text_secondary"],
                bg=COLORS["surface"],
            ).pack()
        
        # Featured Businesses
        tk.Label(
            content,
            text="✨ Featured Businesses",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        # Get real businesses or use placeholders
        all_businesses = queries.get_all_businesses()
        featured = all_businesses[:3] if all_businesses else []
        
        # If no businesses, show placeholders
        if not featured:
            featured = [
                {"name": "Perly's Restaurant & Delicatessen", "category": "Restaurant", "average_rating": "4.8", "description": "Classic deli with a modern twist"},
                {"name": "Quirk Hotel Gallery", "category": "Hotel", "average_rating": "4.7", "description": "Boutique hotel in downtown Richmond"},
                {"name": "Stella's Grocery", "category": "Grocery", "average_rating": "4.9", "description": "Local market and cafe"},
            ]
        
        for biz in featured:
            biz_card = tk.Frame(content, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"], cursor="hand2")
            biz_card.pack(fill=tk.X, pady=(0, SPACING["md"]))
            
            biz_content = tk.Frame(biz_card, bg=COLORS["surface"])
            biz_content.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["lg"])
            
            # Top row
            top = tk.Frame(biz_content, bg=COLORS["surface"])
            top.pack(fill=tk.X, pady=(0, SPACING["sm"]))
            
            tk.Label(
                top,
                text="🏪",
                font=("Segoe UI Emoji", 32),
                bg=COLORS["surface"],
            ).pack(side=tk.LEFT, padx=(0, SPACING["md"]))
            
            info = tk.Frame(top, bg=COLORS["surface"])
            info.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                info,
                text=biz.get("name", "Business"),
                font=FONTS["body_large"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack(anchor=tk.W)
            
            rating_row = tk.Frame(info, bg=COLORS["surface"])
            rating_row.pack(anchor=tk.W)
            
            tk.Label(
                rating_row,
                text=f"⭐ {biz.get('average_rating', '0')}",
                font=FONTS["caption"],
                fg=COLORS["warning"],
                bg=COLORS["surface"],
            ).pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
            
            tk.Label(
                rating_row,
                text=f"• {biz.get('category', 'General')}",
                font=FONTS["caption"],
                fg=COLORS["text_secondary"],
                bg=COLORS["surface"],
            ).pack(side=tk.LEFT)
            
            # Description if available
            desc = biz.get("description", "")
            if desc:
                tk.Label(
                    biz_content,
                    text=desc[:100] + ("..." if len(desc) > 100 else ""),
                    font=FONTS["caption"],
                    fg=COLORS["text_muted"],
                    bg=COLORS["surface"],
                    wraplength=600,
                    justify=tk.LEFT
                ).pack(anchor=tk.W)
            
            # Hover effect
            def on_enter(e, card=biz_card):
                card["bg"] = COLORS["surface_hover"]
            
            def on_leave(e, card=biz_card):
                card["bg"] = COLORS["surface"]
            
            biz_card.bind("<Enter>", on_enter)
            biz_card.bind("<Leave>", on_leave)
            
            if biz.get("id"):
                biz_card.bind("<Button-1>", lambda e, bid=biz["id"]: self._open_business_detail(bid))
        
        # Trending section
        tk.Label(
            content,
            text="🔥 Trending Now",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(SPACING["xl"], SPACING["md"]))
        
        trending_scroll = tk.Frame(content, bg=COLORS["bg"])
        trending_scroll.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        
        trending_items = all_businesses[3:6] if len(all_businesses) > 3 else [
            {"name": "The Roosevelt", "category": "Restaurant", "average_rating": "4.6"},
            {"name": "Can Can Brasserie", "category": "French Cuisine", "average_rating": "4.8"},
            {"name": "Belle Isle", "category": "Park", "average_rating": "4.9"},
        ]
        
        for item in trending_items:
            trending_card = tk.Frame(trending_scroll, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"], width=200)
            trending_card.pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
            trending_card.pack_propagate(False)
            
            card_content = tk.Frame(trending_card, bg=COLORS["surface"])
            card_content.pack(fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
            
            tk.Label(
                card_content,
                text="🔥",
                font=("Segoe UI Emoji", 24),
                bg=COLORS["surface"],
            ).pack(pady=(0, SPACING["xs"]))
            
            tk.Label(
                card_content,
                text=item.get("name", "")[:20],
                font=FONTS["body"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack()
            
            tk.Label(
                card_content,
                text=f"⭐ {item.get('average_rating', '0')}",
                font=FONTS["caption"],
                fg=COLORS["warning"],
                bg=COLORS["surface"],
            ).pack(pady=(SPACING["xs"], 0))
        
        # Quick Actions
        tk.Label(
            content,
            text="Quick Actions",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        actions = [
            {"icon": "📂", "title": "Browse All", "desc": "Explore directory", "cmd": self._show_directory},
            {"icon": "✨", "title": "Recommendations", "desc": "Just for you", "cmd": self._show_recommendations, "color": COLORS["accent"]},
            {"icon": "💰", "title": "Deals", "desc": "Save money", "cmd": self._show_deals, "color": COLORS["success"]},
        ]
        
        for action in actions:
            PremiumCard(
                content,
                icon=action["icon"],
                title=action["title"],
                description=action["desc"],
                command=action["cmd"],
                color_accent=action.get("color")
            ).pack(fill=tk.X, pady=(0, SPACING["sm"]))
    
    def _build_browse_view(self):
        """Complete browse view with search, categories, filters, and business grid."""
        container = tk.Frame(self.content_container, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(
            container,
            text="Browse Businesses",
            font=FONTS["title"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        
        tk.Label(
            container,
            text="Discover local businesses in Richmond, VA",
            font=FONTS["caption"],
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        
        # Search and filter row
        search_row = tk.Frame(container, bg=COLORS["bg"])
        search_row.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        
        search_wrapper = EnhancedEntry(search_row, placeholder="Search businesses...")
        search_wrapper.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, SPACING["sm"]))
        
        filter_btn = tk.Frame(search_row, bg=COLORS["primary"], cursor="hand2", highlightthickness=0)
        filter_btn.pack(side=tk.RIGHT)
        
        tk.Label(
            filter_btn,
            text="🔽 Filter",
            font=FONTS["body"],
            fg=COLORS["surface"],
            bg=COLORS["primary"],
        ).pack(padx=SPACING["md"], pady=SPACING["sm"])
        
        # Category chips
        tk.Label(
            container,
            text="Categories",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        categories_frame = tk.Frame(container, bg=COLORS["bg"])
        categories_frame.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        
        db_categories = queries.get_categories()
        categories = db_categories[:8] if db_categories else ["Food", "Shopping", "Services", "Entertainment", "Health", "Beauty", "Education", "Other"]
        
        category_icons = {"Food": "🍽️", "Shopping": "🛍️", "Services": "🔧", "Entertainment": "🎭", 
                         "Health": "🏥", "Beauty": "💄", "Education": "📚", "Restaurant": "🍴",
                         "Cafe": "☕", "Retail": "🏪", "Hotel": "🏨"}
        
        for i, cat in enumerate(categories):
            icon = category_icons.get(cat, "📍")
            chip = tk.Frame(categories_frame, bg=COLORS["surface"], highlightthickness=1, 
                          highlightbackground=COLORS["border"], cursor="hand2")
            chip.pack(side=tk.LEFT, padx=(0, SPACING["sm"]), pady=(0, SPACING["sm"]))
            
            chip_content = tk.Frame(chip, bg=COLORS["surface"])
            chip_content.pack(padx=SPACING["md"], pady=SPACING["sm"])
            
            tk.Label(
                chip_content,
                text=f"{icon} {cat}",
                font=FONTS["body"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack()
            
            def on_chip_enter(e, c=chip):
                c["bg"] = COLORS["primary_light"]
            
            def on_chip_leave(e, c=chip):
                c["bg"] = COLORS["surface"]
            
            chip.bind("<Enter>", on_chip_enter)
            chip.bind("<Leave>", on_chip_leave)
        
        # Business grid
        tk.Label(
            container,
            text="All Businesses",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        # Get businesses
        all_businesses = queries.get_all_businesses()
        display_businesses = all_businesses[:12] if all_businesses else []
        
        # If no real businesses, use placeholders
        if not display_businesses:
            display_businesses = [
                {"name": "Perly's", "category": "Restaurant", "average_rating": "4.8", "description": "Classic deli"},
                {"name": "Quirk Hotel", "category": "Hotel", "average_rating": "4.7", "description": "Boutique hotel"},
                {"name": "Stella's", "category": "Grocery", "average_rating": "4.9", "description": "Local market"},
                {"name": "The Roosevelt", "category": "Restaurant", "average_rating": "4.6", "description": "Southern comfort"},
                {"name": "Belle Isle", "category": "Park", "average_rating": "4.9", "description": "Outdoor recreation"},
                {"name": "Carytown Books", "category": "Retail", "average_rating": "4.8", "description": "Independent bookstore"},
            ]
        
        for biz in display_businesses:
            biz_card = tk.Frame(container, bg=COLORS["surface"], highlightthickness=1, 
                              highlightbackground=COLORS["border"], cursor="hand2")
            biz_card.pack(fill=tk.X, pady=(0, SPACING["md"]))
            
            biz_content = tk.Frame(biz_card, bg=COLORS["surface"])
            biz_content.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["md"])
            
            # Layout: icon - info - arrow
            icon_label = tk.Label(
                biz_content,
                text=category_icons.get(biz.get("category"), "📍"),
                font=("Segoe UI Emoji", 28),
                bg=COLORS["surface"],
            )
            icon_label.pack(side=tk.LEFT, padx=(0, SPACING["md"]))
            
            info_frame = tk.Frame(biz_content, bg=COLORS["surface"])
            info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(
                info_frame,
                text=biz.get("name", "Business"),
                font=FONTS["body_large"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack(anchor=tk.W)
            
            meta = tk.Frame(info_frame, bg=COLORS["surface"])
            meta.pack(anchor=tk.W)
            
            tk.Label(
                meta,
                text=f"⭐ {biz.get('average_rating', '0')}",
                font=FONTS["caption"],
                fg=COLORS["warning"],
                bg=COLORS["surface"],
            ).pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
            
            tk.Label(
                meta,
                text=f"• {biz.get('category', 'General')}",
                font=FONTS["caption"],
                fg=COLORS["text_secondary"],
                bg=COLORS["surface"],
            ).pack(side=tk.LEFT)
            
            if biz.get("description"):
                tk.Label(
                    info_frame,
                    text=biz["description"][:60] + ("..." if len(biz["description"]) > 60 else ""),
                    font=FONTS["caption"],
                    fg=COLORS["text_muted"],
                    bg=COLORS["surface"],
                ).pack(anchor=tk.W)
            
            tk.Label(
                biz_content,
                text="→",
                font=FONTS["heading"],
                fg=COLORS["text_muted"],
                bg=COLORS["surface"],
            ).pack(side=tk.RIGHT)
            
            def on_biz_enter(e, card=biz_card):
                card["bg"] = COLORS["surface_hover"]
            
            def on_biz_leave(e, card=biz_card):
                card["bg"] = COLORS["surface"]
            
            biz_card.bind("<Enter>", on_biz_enter)
            biz_card.bind("<Leave>", on_biz_leave)
            
            if biz.get("id"):
                biz_card.bind("<Button-1>", lambda e, bid=biz["id"]: self._open_business_detail(bid))
        
        # View all button
        view_all_card = tk.Frame(container, bg=COLORS["primary_light"], cursor="hand2", highlightthickness=0)
        view_all_card.pack(fill=tk.X, pady=(SPACING["lg"], 0))
        
        tk.Label(
            view_all_card,
            text="📂 View Full Directory",
            font=FONTS["subheading"],
            fg=COLORS["primary"],
            bg=COLORS["primary_light"],
        ).pack(pady=SPACING["lg"])
        
        view_all_card.bind("<Button-1>", lambda e: self._show_directory())
    
    def _build_favorites_view(self):
        """Complete favorites view with grid or empty state."""
        container = tk.Frame(self.content_container, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Header
        tk.Label(
            container,
            text="My Favorites",
            font=FONTS["title"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        
        user_id = self.user.get("id")
        favorite_ids = queries.get_favorite_business_ids(user_id) if user_id else []
        
        tk.Label(
            container,
            text=f"{len(favorite_ids)} saved businesses",
            font=FONTS["caption"],
            fg=COLORS["text_secondary"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["xl"]))
        
        if favorite_ids:
            # Display favorites
            for biz_id in favorite_ids:
                biz = queries.get_business_by_id(biz_id)
                if biz:
                    fav_card = tk.Frame(container, bg=COLORS["surface"], highlightthickness=1, 
                                       highlightbackground=COLORS["border"], cursor="hand2")
                    fav_card.pack(fill=tk.X, pady=(0, SPACING["md"]))
                    
                    card_content = tk.Frame(fav_card, bg=COLORS["surface"])
                    card_content.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["md"])
                    
                    # Icon
                    tk.Label(
                        card_content,
                        text="❤️",
                        font=("Segoe UI Emoji", 32),
                        bg=COLORS["surface"],
                    ).pack(side=tk.LEFT, padx=(0, SPACING["md"]))
                    
                    # Info
                    info = tk.Frame(card_content, bg=COLORS["surface"])
                    info.pack(side=tk.LEFT, fill=tk.X, expand=True)
                    
                    tk.Label(
                        info,
                        text=biz.get("name", "Business"),
                        font=FONTS["body_large"],
                        fg=COLORS["text"],
                        bg=COLORS["surface"],
                    ).pack(anchor=tk.W)
                    
                    meta = tk.Frame(info, bg=COLORS["surface"])
                    meta.pack(anchor=tk.W)
                    
                    tk.Label(
                        meta,
                        text=f"⭐ {biz.get('average_rating', '0')}",
                        font=FONTS["caption"],
                        fg=COLORS["warning"],
                        bg=COLORS["surface"],
                    ).pack(side=tk.LEFT, padx=(0, SPACING["sm"]))
                    
                    tk.Label(
                        meta,
                        text=f"• {biz.get('category', 'General')}",
                        font=FONTS["caption"],
                        fg=COLORS["text_secondary"],
                        bg=COLORS["surface"],
                    ).pack(side=tk.LEFT)
                    
                    # Arrow
                    tk.Label(
                        card_content,
                        text="→",
                        font=FONTS["heading"],
                        fg=COLORS["text_muted"],
                        bg=COLORS["surface"],
                    ).pack(side=tk.RIGHT)
                    
                    def on_enter(e, card=fav_card):
                        card["bg"] = COLORS["surface_hover"]
                    
                    def on_leave(e, card=fav_card):
                        card["bg"] = COLORS["surface"]
                    
                    fav_card.bind("<Enter>", on_enter)
                    fav_card.bind("<Leave>", on_leave)
                    fav_card.bind("<Button-1>", lambda e, bid=biz_id: self._open_business_detail(bid))
        else:
            # Empty state
            empty = tk.Frame(container, bg=COLORS["bg"])
            empty.pack(fill=tk.BOTH, expand=True, pady=SPACING["xxl"])
            
            tk.Label(
                empty,
                text="💔",
                font=("Segoe UI Emoji", 64),
                fg=COLORS["text_muted"],
                bg=COLORS["bg"],
            ).pack(pady=(SPACING["xxl"], SPACING["lg"]))
            
            tk.Label(
                empty,
                text="No favorites yet",
                font=FONTS["heading"],
                fg=COLORS["text_secondary"],
                bg=COLORS["bg"],
            ).pack(pady=(0, SPACING["sm"]))
            
            tk.Label(
                empty,
                text="Start exploring and save your favorite businesses",
                font=FONTS["body"],
                fg=COLORS["text_muted"],
                bg=COLORS["bg"],
            ).pack(pady=(0, SPACING["xl"]))
            
            # Action button
            empty_btn = tk.Frame(empty, bg=COLORS["primary"], cursor="hand2", highlightthickness=0)
            empty_btn.pack()
            
            tk.Label(
                empty_btn,
                text="📂 Browse Businesses",
                font=FONTS["body_large"],
                fg=COLORS["surface"],
                bg=COLORS["primary"],
            ).pack(padx=SPACING["xl"], pady=SPACING["lg"])
            
            empty_btn.bind("<Button-1>", lambda e: self._show_directory())
    
    def _build_profile_view(self):
        """Complete profile/account view with header, stats, and actions."""
        container = tk.Frame(self.content_container, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
        container.pack(fill=tk.BOTH, expand=True)
        
        # Profile header card
        header = tk.Frame(container, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
        header.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        
        header_content = tk.Frame(header, bg=COLORS["surface"])
        header_content.pack(fill=tk.X, padx=SPACING["xl"], pady=SPACING["xl"])
        
        # Avatar
        username = self.user.get("username", self.user.get("email", "User"))
        initials = username[0:2].upper() if len(username) > 1 else username[0].upper()
        
        avatar = tk.Label(
            header_content,
            text=initials,
            font=("Segoe UI", 42, "bold"),
            fg=COLORS["surface"],
            bg=COLORS["primary"],
            width=4,
            height=2,
        )
        avatar.pack(pady=(0, SPACING["lg"]))
        
        tk.Label(
            header_content,
            text=username,
            font=FONTS["heading"],
            fg=COLORS["text"],
            bg=COLORS["surface"],
        ).pack()
        
        tk.Label(
            header_content,
            text=self.user.get("email", ""),
            font=FONTS["caption"],
            fg=COLORS["text_secondary"],
            bg=COLORS["surface"],
        ).pack(pady=(SPACING["xs"], SPACING["sm"]))
        
        tk.Label(
            header_content,
            text="📍 Richmond, VA",
            font=FONTS["caption"],
            fg=COLORS["text_muted"],
            bg=COLORS["surface"],
        ).pack()
        
        # Stats row
        tk.Label(
            container,
            text="Activity",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        user_stats = queries.get_user_stats(self.user.get("id"))
        
        stats_row = tk.Frame(container, bg=COLORS["bg"])
        stats_row.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        
        stats = [
            {"label": "Favorites", "value": str(user_stats["favorite_count"]), "icon": "❤️"},
            {"label": "Reviews", "value": str(user_stats["review_count"]), "icon": "📝"},
            {"label": "Avg Rating", "value": str(user_stats["avg_rating_given"]), "icon": "⭐"},
        ]
        
        for i, stat in enumerate(stats):
            stat_card = tk.Frame(stats_row, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, SPACING["sm"] if i < 2 else 0))
            
            stat_content = tk.Frame(stat_card, bg=COLORS["surface"])
            stat_content.pack(fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["lg"])
            
            tk.Label(
                stat_content,
                text=stat["icon"],
                font=("Segoe UI Emoji", 24),
                bg=COLORS["surface"],
            ).pack()
            
            tk.Label(
                stat_content,
                text=stat["value"],
                font=FONTS["heading"],
                fg=COLORS["text"],
                bg=COLORS["surface"],
            ).pack(pady=(SPACING["xs"], 0))
            
            tk.Label(
                stat_content,
                text=stat["label"],
                font=FONTS["caption"],
                fg=COLORS["text_secondary"],
                bg=COLORS["surface"],
            ).pack()
        
        # Account actions
        tk.Label(
            container,
            text="Account",
            font=FONTS["subheading"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        actions = [
            {"icon": "⚙️", "title": "Account Settings", "desc": "Change password and preferences", "cmd": self._open_account_settings, "color": COLORS["accent"]},
            {"icon": "❤️", "title": "My Favorites", "desc": "View saved businesses", "cmd": lambda: self._handle_nav_click("favorites"), "color": COLORS["danger"]},
            {"icon": "📝", "title": "My Reviews", "desc": "See all your reviews", "cmd": self._show_my_reviews},
            {"icon": "❓", "title": "Help & Support", "desc": "Get assistance", "cmd": self._show_help, "color": COLORS["info"]},
            {"icon": "🗃️", "title": "Verification History", "desc": "View verification logs", "cmd": self._show_verification_table, "color": COLORS["secondary"]},
        ]
        
        for action in actions:
            PremiumCard(
                container,
                icon=action["icon"],
                title=action["title"],
                description=action["desc"],
                command=action["cmd"],
                color_accent=action.get("color")
            ).pack(fill=tk.X, pady=(0, SPACING["md"]))
        
        # Logout
        logout_card = tk.Frame(container, bg=COLORS["danger_light"], cursor="hand2", highlightthickness=0)
        logout_card.pack(fill=tk.X, pady=(SPACING["lg"], 0))
        
        tk.Label(
            logout_card,
            text="🚪 Exit Application",
            font=FONTS["subheading"],
            fg=COLORS["danger"],
            bg=COLORS["danger_light"],
        ).pack(pady=SPACING["lg"])
        
        logout_card.bind("<Button-1>", lambda e: self.win.destroy())
    
    def _open_account_settings(self):
        """Open account settings window."""
        def on_update(updated_user):
            self.user.update(updated_user)
            for widget in self.content_container.winfo_children():
                widget.destroy()
            self.canvas.yview_moveto(0)
            self._build_profile_view()
        
        open_account_settings(self.win, self.user, on_update=on_update)
    
    def _open_business_detail(self, business_id):
        """Open business detail window."""
        from src.ui.directory_window import open_business_detail
        open_business_detail(self.win, self.user, business_id)
    
    def _show_directory(self):
        open_directory(self.win, self.user)

    def _show_deals(self):
        open_deals(self.win, self.user)

    def _show_trending(self):
        open_trending(self.win, self.user)

    def _show_my_reviews(self):
        open_my_reviews(self.win, self.user)

    def _show_help(self):
        open_help(self.win)

    def _show_recommendations(self):
        open_recommendations(self.win, self.user)

    def _show_verification_table(self):
        """Open verification history window."""
        rows = queries.get_all_verification_attempts()
        top = tk.Toplevel(self.win)
        top.title("Hidden Gems — Verification History")
        top.geometry("900x480")
        apply_window_bg(top)
        
        f = tk.Frame(top, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
        f.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            f,
            text="Verification History",
            font=FONTS["heading"],
            fg=COLORS["text"],
            bg=COLORS["bg"]
        ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
        
        if not rows:
            tk.Label(
                f,
                text="No verification attempts yet.",
                font=FONTS["caption"],
                fg=COLORS["text_secondary"],
                bg=COLORS["bg"]
            ).pack(anchor=tk.W)
            return
        
        table_frame = tk.Frame(f, bg=COLORS["surface"], highlightthickness=1, highlightbackground=COLORS["border"])
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        columns = ("id", "email", "verification_type", "question", "correct_answer", "user_answer", "success", "attempted_at", "context")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=90)
        tree.column("question", width=180)
        tree.column("attempted_at", width=160)
        scroll = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        for r in rows:
            tree.insert("", tk.END, values=(
                r.get("id"),
                r.get("email"),
                r.get("verification_type"),
                r.get("question"),
                r.get("correct_answer"),
                r.get("user_answer"),
                "✓" if r.get("success") else "✗",
                r.get("attempted_at"),
                r.get("context"),
            ))
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=SPACING["md"], pady=SPACING["md"])
        scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=SPACING["md"], padx=(0, SPACING["md"]))

    def run(self):
        self.win.mainloop()


def show_main_menu(user):
    app = MainMenuWindow(user)
    app.run()
