import os
import tkinter as tk
from tkinter import messagebox, ttk
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing Supabase credentials. Please set SUPABASE_URL and SUPABASE_KEY in your .env file."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class LoginFrame(ttk.Frame):
    def __init__(self, parent, on_success_callback):
        super().__init__(parent, padding="20")
        self.parent = parent
        self.on_success = on_success_callback  # This function runs when login succeeds
        
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self, text="KRAWL SECURE MESSENGER", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(self, text="Username:").pack(anchor=tk.W, pady=(5, 0))
        self.email_entry = ttk.Entry(self, width=30)
        self.email_entry.pack(fill=tk.X, pady=5)

        ttk.Label(self, text="Password:").pack(anchor=tk.W, pady=(5, 0))
        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack(fill=tk.X, pady=5)

        self.login_btn = ttk.Button(self, text="Login", command=self.handle_login)
        self.login_btn.pack(pady=15, fill=tk.X)

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        self.login_btn.config(state=tk.DISABLED)
        
        try:
            auth_response = supabase.auth.sign_in_with_password({"email": email, "password": password})
            user = auth_response.user
            
            if user:
                # Send the user ID and email back to app.py
                self.on_success(user.id, email)
                
        except Exception as e:
            messagebox.showerror("Access Denied", f"Unauthorized account or invalid credentials.\n error code: {e}")
            self.login_btn.config(state=tk.NORMAL)