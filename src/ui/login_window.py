"""
Login and Register - separate pages with email verification (sends real email when SMTP configured).
Hidden Gems | FBLA 2026
"""
import tkinter as tk
from tkinter import ttk, messagebox

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import random
import string

from src.logic import auth
from src.logic.email_sender import is_email_configured, send_verification_email
from src.database import queries
from src.verification.verifier import get_challenge, verify_and_log
from src.ui.theme import COLORS, FONTS, apply_window_bg
from src.ui.design_system import LAYOUT, SPACING
from src.ui.components import (
    make_centered_card,
    PrimaryButton,
    SecondaryButton,
    ModernEntry,
    ModernLabel,
)


def _generate_email_code():
    """Generate a 6-digit numeric code for email verification."""
    return "".join(random.choices(string.digits, k=6))


class LoginWindow:
    def __init__(self, on_login_success):
        self.on_login_success = on_login_success
        self.current_user_email = None
        self.current_user_id = None
        self.current_question = None
        self.current_correct = None
        self.win = tk.Tk()
        self.win.title("Hidden Gems")
        self.win.geometry("520x580+100+100")
        self.win.minsize(440, 520)
        self.win.resizable(True, True)
        apply_window_bg(self.win)
        self._container, self._center = make_centered_card(
            self.win,
            max_width=LAYOUT["content_max_width"],
            outer_pad=SPACING["xl"],
        )
        self._build_welcome_frame()
        self._build_login_frame()
        self._build_register_frame()
        self._build_email_verification_frame()
        self._build_verification_frame()
        self._show_welcome()
        self._bring_to_front()

    def _bring_to_front(self):
        """Force window on-screen and to the front (helps when it opens off-screen or behind others)."""
        self.win.update_idletasks()
        # If window ended up off-screen, move to top-left of primary screen
        try:
            x = self.win.winfo_x()
            y = self.win.winfo_y()
            w = self.win.winfo_screenwidth()
            h = self.win.winfo_screenheight()
            if x < 0 or y < 0 or x > w - 100 or y > h - 100:
                self.win.geometry("420x460+50+50")
        except Exception:
            self.win.geometry("420x460+50+50")
        self.win.lift()
        self.win.attributes("-topmost", True)
        self.win.after(200, lambda: self.win.attributes("-topmost", False))
        self.win.focus_force()

    def _hide_all(self):
        for f in (
            self.welcome_frame,
            self.login_frame,
            self.register_frame,
            self.email_verification_frame,
            self.verification_frame,
        ):
            f.pack_forget()

    def _show_welcome(self):
        self._hide_all()
        self.welcome_frame.pack(fill=tk.BOTH, expand=True)

    def _show_login(self):
        self._hide_all()
        self.login_frame.pack(fill=tk.BOTH, expand=True)
        self.entry_login_email.entry.focus_set()

    def _show_register(self):
        self._hide_all()
        self.register_frame.pack(fill=tk.BOTH, expand=True)
        self.entry_register_username.entry.focus_set()

    def _show_email_verification(self, user_id, email, is_after_register=True):
        self._hide_all()
        self.email_verification_frame.pack(fill=tk.BOTH, expand=True)
        self.current_user_id = user_id
        self.current_user_email = email
        code = _generate_email_code()
        if not is_after_register:
            latest = queries.get_latest_verification_code(user_id)
            if latest:
                code = latest
            else:
                queries.create_email_verification_code(user_id, code)
        else:
            queries.create_email_verification_code(user_id, code)

        sent, err = send_verification_email(email, code)
        if sent:
            self.lbl_email_verify_msg.config(
                text=f"We've sent a verification code to {email}.\nCheck your inbox and enter the code below."
            )
            self.lbl_demo_code.config(text="")
        else:
            self.lbl_email_verify_msg.config(
                text="Email sending is not set up (no SMTP config),\nso use the code below to verify your account."
            )
            self.lbl_demo_code.config(text=f"Your code: {code}", fg="gray")
        self.entry_email_code.entry.delete(0, tk.END)
        self.entry_email_code.entry.focus_set()

    def _show_verification(self):
        self._hide_all()
        self.verification_frame.pack(fill=tk.BOTH, expand=True)
        self.current_question, self.current_correct = get_challenge()
        self.lbl_verification_question.config(text=self.current_question)
        self.entry_verification_answer.entry.delete(0, tk.END)
        self.entry_verification_answer.entry.focus_set()

    # ---------- Welcome ----------
    def _build_welcome_frame(self):
        self.welcome_frame = tk.Frame(self._center, bg=COLORS["surface"])
        
        # Icon / visual element
        icon = tk.Label(
            self.welcome_frame,
            text="💎",
            font=("Segoe UI Emoji", 52, "normal"),
            fg=COLORS["primary"],
            bg=COLORS["surface"],
        )
        icon.pack(pady=(SPACING["xxl"], SPACING["lg"]))
        
        ModernLabel(self.welcome_frame, text="Hidden Gems", style="title").pack(pady=(0, SPACING["sm"]))
        ModernLabel(self.welcome_frame, text="Discover & support local businesses", style="caption").pack(pady=(0, SPACING["xs"]))
        ModernLabel(self.welcome_frame, text="Richmond, Virginia", style="caption").pack(pady=(0, SPACING["xxl"] + SPACING["md"]))
        
        PrimaryButton(self.welcome_frame, text="Log in", command=self._show_login).pack(fill=tk.X, pady=SPACING["md"])
        PrimaryButton(self.welcome_frame, text="Create account", command=self._show_register).pack(fill=tk.X, pady=SPACING["sm"])

    # ---------- Login ----------
    def _build_login_frame(self):
        self.login_frame = tk.Frame(self._center, bg=COLORS["surface"])
        
        # Back link
        back = tk.Label(
            self.login_frame, text="← Back",
            font=FONTS["caption"], fg=COLORS["primary"],
            cursor="hand2", bg=COLORS["surface"],
        )
        back.pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        back.bind("<Button-1>", lambda e: self._show_welcome())
        back.bind("<Enter>", lambda e: back.config(font=(FONTS["caption"][0], FONTS["caption"][1], "underline")))
        back.bind("<Leave>", lambda e: back.config(font=FONTS["caption"]))
        
        ModernLabel(self.login_frame, text="Log in", style="heading").pack(pady=(0, SPACING["xxl"]))
        ModernLabel(self.login_frame, text="Email or username", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_login_email = ModernEntry(self.login_frame)
        self.entry_login_email.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        ModernLabel(self.login_frame, text="Password", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_login_password = ModernEntry(self.login_frame, show="*")
        self.entry_login_password.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        PrimaryButton(self.login_frame, text="Log in", command=self._do_login).pack(fill=tk.X, pady=SPACING["md"])
        
        # Link
        link_frame = tk.Frame(self.login_frame, bg=COLORS["surface"])
        link_frame.pack(pady=(SPACING["xl"], 0))
        ModernLabel(link_frame, text="Don't have an account?", style="caption").pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        link_register = tk.Label(
            link_frame, text="Create account",
            fg=COLORS["primary"], font=FONTS["body"],
            cursor="hand2", bg=COLORS["surface"], highlightthickness=0,
        )
        link_register.pack(side=tk.LEFT)
        link_register.bind("<Button-1>", lambda e: self._show_register())
        link_register.bind("<Enter>", lambda e: link_register.config(fg=COLORS["primary_hover"], font=(FONTS["body"][0], FONTS["body"][1], "underline")))
        link_register.bind("<Leave>", lambda e: link_register.config(fg=COLORS["primary"], font=FONTS["body"]))

    # ---------- Register ----------
    def _build_register_frame(self):
        self.register_frame = tk.Frame(self._center, bg=COLORS["surface"])
        
        # Back link
        back = tk.Label(
            self.register_frame, text="← Back",
            font=FONTS["caption"], fg=COLORS["primary"],
            cursor="hand2", bg=COLORS["surface"],
        )
        back.pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        back.bind("<Button-1>", lambda e: self._show_welcome())
        back.bind("<Enter>", lambda e: back.config(font=(FONTS["caption"][0], FONTS["caption"][1], "underline")))
        back.bind("<Leave>", lambda e: back.config(font=FONTS["caption"]))
        
        ModernLabel(self.register_frame, text="Create account", style="heading").pack(pady=(0, SPACING["xxl"]))
        ModernLabel(self.register_frame, text="Username", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_register_username = ModernEntry(self.register_frame)
        self.entry_register_username.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        ModernLabel(self.register_frame, text="Email", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_register_email = ModernEntry(self.register_frame)
        self.entry_register_email.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        ModernLabel(self.register_frame, text="Password", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_register_password = ModernEntry(self.register_frame, show="*")
        self.entry_register_password.pack(fill=tk.X, pady=(0, SPACING["lg"]))
        ModernLabel(self.register_frame, text="Confirm password", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_register_confirm = ModernEntry(self.register_frame, show="*")
        self.entry_register_confirm.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        PrimaryButton(self.register_frame, text="Create account", command=self._do_register).pack(fill=tk.X, pady=SPACING["md"])
        
        # Link
        link_frame = tk.Frame(self.register_frame, bg=COLORS["surface"])
        link_frame.pack(pady=(SPACING["xl"], 0))
        ModernLabel(link_frame, text="Already have an account?", style="caption").pack(side=tk.LEFT, padx=(0, SPACING["xs"]))
        link_login = tk.Label(
            link_frame, text="Log in",
            fg=COLORS["primary"], font=FONTS["body"],
            cursor="hand2", bg=COLORS["surface"], highlightthickness=0,
        )
        link_login.pack(side=tk.LEFT)
        link_login.bind("<Button-1>", lambda e: self._show_login())
        link_login.bind("<Enter>", lambda e: link_login.config(fg=COLORS["primary_hover"], font=(FONTS["body"][0], FONTS["body"][1], "underline")))
        link_login.bind("<Leave>", lambda e: link_login.config(fg=COLORS["primary"], font=FONTS["body"]))

    # ---------- Email verification ----------
    def _build_email_verification_frame(self):
        self.email_verification_frame = tk.Frame(self._center, bg=COLORS["surface"])
        
        icon = tk.Label(
            self.email_verification_frame,
            text="📧",
            font=("Segoe UI Emoji", 42, "normal"),
            fg=COLORS["info"],
            bg=COLORS["surface"],
        )
        icon.pack(pady=(SPACING["xl"], SPACING["lg"]))
        
        ModernLabel(self.email_verification_frame, text="Verify your email", style="heading").pack(pady=(0, SPACING["md"]))
        self.lbl_email_verify_msg = ModernLabel(self.email_verification_frame, text="", style="caption")
        self.lbl_email_verify_msg.pack(anchor=tk.W, pady=(0, SPACING["sm"]))
        self.lbl_demo_code = tk.Label(self.email_verification_frame, text="", font=FONTS["caption"], fg=COLORS["text_muted"], bg=COLORS["surface"])
        self.lbl_demo_code.pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        ModernLabel(self.email_verification_frame, text="Verification code", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_email_code = ModernEntry(self.email_verification_frame)
        self.entry_email_code.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        self.entry_email_code.entry.bind("<Return>", lambda e: self._do_verify_email())
        PrimaryButton(self.email_verification_frame, text="Verify email", command=self._do_verify_email).pack(fill=tk.X, pady=SPACING["md"])
        
        # Back button as link
        back_link = tk.Label(
            self.email_verification_frame, text="← Go back",
            font=FONTS["caption"], fg=COLORS["secondary"],
            cursor="hand2", bg=COLORS["surface"],
        )
        back_link.pack(pady=(SPACING["md"], 0))
        back_link.bind("<Button-1>", lambda e: self._back_from_email_verify())
        back_link.bind("<Enter>", lambda e: back_link.config(font=(FONTS["caption"][0], FONTS["caption"][1], "underline")))
        back_link.bind("<Leave>", lambda e: back_link.config(font=FONTS["caption"]))

    def _back_from_email_verify(self):
        self._show_login()

    # ---------- Bot verification ----------
    def _build_verification_frame(self):
        self.verification_frame = tk.Frame(self._center, bg=COLORS["surface"])
        
        icon = tk.Label(
            self.verification_frame,
            text="🔒",
            font=("Segoe UI Emoji", 42, "normal"),
            fg=COLORS["warning"],
            bg=COLORS["surface"],
        )
        icon.pack(pady=(SPACING["xl"], SPACING["lg"]))
        
        ModernLabel(self.verification_frame, text="One more step", style="heading").pack(pady=(0, SPACING["lg"]))
        self.lbl_verification_question = ModernLabel(self.verification_frame, text="", style="body")
        self.lbl_verification_question.pack(anchor=tk.W, pady=(0, SPACING["lg"]))
        ModernLabel(self.verification_frame, text="Your answer", style="caption").pack(anchor=tk.W, pady=(0, SPACING["xs"]))
        self.entry_verification_answer = ModernEntry(self.verification_frame)
        self.entry_verification_answer.pack(fill=tk.X, pady=(0, SPACING["xl"]))
        self.entry_verification_answer.entry.bind("<Return>", lambda e: self._do_verify_and_login())
        PrimaryButton(self.verification_frame, text="Verify & Log in", command=self._do_verify_and_login).pack(fill=tk.X, pady=SPACING["md"])
        
        # Back link
        back_link = tk.Label(
            self.verification_frame, text="← Go back",
            font=FONTS["caption"], fg=COLORS["secondary"],
            cursor="hand2", bg=COLORS["surface"],
        )
        back_link.pack(pady=(SPACING["md"], 0))
        back_link.bind("<Button-1>", lambda e: self._show_login())
        back_link.bind("<Enter>", lambda e: back_link.config(font=(FONTS["caption"][0], FONTS["caption"][1], "underline")))
        back_link.bind("<Leave>", lambda e: back_link.config(font=FONTS["caption"]))

    # ---------- Actions ----------
    def _do_login(self):
        identifier = self.entry_login_email.entry.get().strip()
        password = self.entry_login_password.entry.get()
        ok, result = auth.validate_login(identifier, password)
        if not ok:
            if result == "EMAIL_NOT_VERIFIED":
                user = queries.user_by_email_or_username(identifier)
                if user:
                    self._show_email_verification(user["id"], user["email"], is_after_register=False)
                else:
                    messagebox.showerror("Login failed", "No account found.")
            else:
                messagebox.showerror("Login failed", result)
            return
        self.current_login_identifier = identifier
        self.current_user_email = result["email"]
        self._show_verification()

    def _do_register(self):
        username = self.entry_register_username.entry.get().strip()
        email = self.entry_register_email.entry.get().strip()
        password = self.entry_register_password.entry.get()
        confirm = self.entry_register_confirm.entry.get()
        if password != confirm:
            messagebox.showerror("Registration failed", "Passwords do not match.")
            return
        ok, result = auth.register_user(username, email, password)
        if not ok:
            messagebox.showerror("Registration failed", result)
            return
        self._show_email_verification(result, email, is_after_register=True)

    def _do_verify_email(self):
        code = self.entry_email_code.entry.get().strip()
        if not code:
            messagebox.showwarning("Missing code", "Please enter the verification code.")
            return
        if not self.current_user_id:
            messagebox.showerror("Error", "Session lost. Please try again from the login screen.")
            self._show_login()
            return
        if queries.validate_email_code(self.current_user_id, code):
            messagebox.showinfo("Email verified", "Your email is verified. You can now log in.")
            self._show_login()
        else:
            messagebox.showerror("Invalid code", "That code is incorrect or expired. Please try again.")

    def _do_verify_and_login(self):
        answer = self.entry_verification_answer.entry.get()
        if not self.current_question or not self.current_correct:
            messagebox.showwarning("Error", "Verification challenge missing. Try again.")
            self._show_login()
            return
        success = verify_and_log(
            self.current_user_email or self.current_login_identifier,
            answer,
            self.current_question,
            self.current_correct,
            context="login",
        )
        if not success:
            messagebox.showerror("Verification failed", "Incorrect. Please try again or go back.")
            self._show_verification()
            return
        password = self.entry_login_password.entry.get()
        ok, user = auth.validate_login(self.current_login_identifier, password)
        if ok:
            self.win.destroy()
            self.on_login_success(user)
        else:
            messagebox.showerror("Error", "Login could not be completed.")
            self._show_login()

    def run(self):
        self.win.mainloop()


def show_login(on_login_success):
    app = LoginWindow(on_login_success)
    app.run()
