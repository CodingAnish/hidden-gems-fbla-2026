"""
Account settings window — password change, email change, profile editing.
FBLA 2026 Hidden Gems.
"""
import tkinter as tk
from tkinter import messagebox
import hashlib

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from src.database import queries
from src.verification.verifier import get_challenge, verify_and_log
from src.ui.design_system import COLORS, FONTS, SPACING
from src.ui.components import PremiumCard, ModernEntry, ModernLabel, ToastNotification


def open_account_settings(parent, user, on_update=None):
    """Open account settings window."""
    top = tk.Toplevel(parent)
    top.title("Hidden Gems — Account Settings")
    top.geometry("580x700")
    top.configure(bg=COLORS["bg"])
    
    container = tk.Frame(top, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
    container.pack(fill=tk.BOTH, expand=True)
    
    # Title
    tk.Label(
        container,
        text="Account Settings",
        font=FONTS["title"],
        fg=COLORS["text"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["lg"]))
    
    # Current info card
    info_card = tk.Frame(
        container,
        bg=COLORS["surface"],
        highlightthickness=1,
        highlightbackground=COLORS["border"]
    )
    info_card.pack(fill=tk.X, pady=(0, SPACING["xl"]))
    
    info_content = tk.Frame(info_card, bg=COLORS["surface"])
    info_content.pack(fill=tk.X, padx=SPACING["lg"], pady=SPACING["lg"])
    
    tk.Label(
        info_content,
        text="Current Information",
        font=FONTS["subheading"],
        fg=COLORS["text"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
    
    tk.Label(
        info_content,
        text=f"Username: {user.get('username', 'N/A')}",
        font=FONTS["body"],
        fg=COLORS["text_secondary"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    tk.Label(
        info_content,
        text=f"Email: {user.get('email', 'N/A')}",
        font=FONTS["body"],
        fg=COLORS["text_secondary"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    tk.Label(
        info_content,
        text=f"Member since: {user.get('created_date', 'N/A')}",
        font=FONTS["caption"],
        fg=COLORS["text_muted"],
        bg=COLORS["surface"],
    ).pack(anchor=tk.W)
    
    # Change username
    tk.Label(
        container,
        text="Change Username",
        font=FONTS["subheading"],
        fg=COLORS["text"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
    
    tk.Label(
        container,
        text="New username",
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    username_entry = ModernEntry(container)
    username_entry.pack(fill=tk.X, pady=(0, SPACING["md"]))
    username_entry.entry.insert(0, user.get('username', ''))
    
    def change_username():
        new_username = username_entry.entry.get().strip()
        if not new_username:
            ToastNotification.show(top, "Username cannot be empty", "error")
            return
        if new_username == user.get('username'):
            ToastNotification.show(top, "Username unchanged", "info")
            return
        
        # Update in database
        user_id = user.get('id')
        if user_id:
            queries.update_user_username(user_id, new_username)
            user['username'] = new_username
            ToastNotification.show(top, "Username updated successfully!", "success")
            if on_update:
                on_update(user)
    
    PremiumCard(
        container,
        icon="✏️",
        title="Update Username",
        description="Save your new username",
        command=change_username,
        color_accent=COLORS["accent"],
        show_arrow=False
    ).pack(fill=tk.X, pady=(0, SPACING["xl"]))
    
    # Change password
    tk.Label(
        container,
        text="Change Password",
        font=FONTS["subheading"],
        fg=COLORS["text"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["md"]))
    
    tk.Label(
        container,
        text="Current password",
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    current_pw_entry = ModernEntry(container, show="*")
    current_pw_entry.pack(fill=tk.X, pady=(0, SPACING["md"]))
    
    tk.Label(
        container,
        text="New password",
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    new_pw_entry = ModernEntry(container, show="*")
    new_pw_entry.pack(fill=tk.X, pady=(0, SPACING["md"]))
    
    tk.Label(
        container,
        text="Confirm new password",
        font=FONTS["caption"],
        fg=COLORS["text_secondary"],
        bg=COLORS["bg"],
    ).pack(anchor=tk.W, pady=(0, SPACING["xs"]))
    
    confirm_pw_entry = ModernEntry(container, show="*")
    confirm_pw_entry.pack(fill=tk.X, pady=(0, SPACING["md"]))
    
    def change_password():
        current = current_pw_entry.entry.get()
        new = new_pw_entry.entry.get()
        confirm = confirm_pw_entry.entry.get()
        
        if not current or not new or not confirm:
            ToastNotification.show(top, "All password fields are required", "error")
            return
        
        if new != confirm:
            ToastNotification.show(top, "New passwords don't match", "error")
            return
        
        if len(new) < 4:
            ToastNotification.show(top, "Password must be at least 4 characters", "error")
            return
        
        # Verify current password
        current_hash = hashlib.sha256(current.encode()).hexdigest()
        if current_hash != user.get('password_hash'):
            ToastNotification.show(top, "Current password is incorrect", "error")
            return
        
        # Verification challenge
        q, a = get_challenge()
        verify_top = tk.Toplevel(top)
        verify_top.title("Verify Password Change")
        verify_top.geometry("420x220")
        verify_top.configure(bg=COLORS["bg"])
        
        verify_container = tk.Frame(verify_top, bg=COLORS["bg"], padx=SPACING["xl"], pady=SPACING["xl"])
        verify_container.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(
            verify_container,
            text="🔒",
            font=("Segoe UI Emoji", 42, "normal"),
            fg=COLORS["warning"],
            bg=COLORS["bg"],
        ).pack(pady=(0, SPACING["lg"]))
        
        tk.Label(
            verify_container,
            text=q,
            font=FONTS["body"],
            fg=COLORS["text"],
            bg=COLORS["bg"],
        ).pack(pady=(0, SPACING["md"]))
        
        answer_entry = ModernEntry(verify_container)
        answer_entry.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        
        def verify_and_update():
            user_ans = answer_entry.entry.get().strip()
            ok = verify_and_log(user.get("email") or "", user_ans, q, a, "password_change")
            verify_top.destroy()
            
            if ok:
                # Update password
                new_hash = hashlib.sha256(new.encode()).hexdigest()
                user_id = user.get('id')
                if user_id:
                    queries.update_user_password(user_id, new_hash)
                    user['password_hash'] = new_hash
                    current_pw_entry.entry.delete(0, tk.END)
                    new_pw_entry.entry.delete(0, tk.END)
                    confirm_pw_entry.entry.delete(0, tk.END)
                    ToastNotification.show(top, "Password changed successfully!", "success")
            else:
                ToastNotification.show(top, "Verification failed", "error")
        
        PremiumCard(
            verify_container,
            icon="✓",
            title="Verify & Change Password",
            description="Confirm your answer",
            command=verify_and_update,
            color_accent=COLORS["primary"],
            show_arrow=False
        ).pack(fill=tk.X)
    
    PremiumCard(
        container,
        icon="🔒",
        title="Update Password",
        description="Secure your account with a new password",
        command=change_password,
        color_accent=COLORS["warning"],
        show_arrow=False
    ).pack(fill=tk.X, pady=(0, SPACING["lg"]))
    
    # Close button
    close_card = tk.Frame(container, bg=COLORS["bg"])
    close_card.pack(fill=tk.X, pady=(SPACING["md"], 0))
    
    PremiumCard(
        close_card,
        icon="←",
        title="Close",
        description="Return to profile",
        command=top.destroy,
        color_accent=COLORS["secondary"],
        show_arrow=False
    ).pack(fill=tk.X)
