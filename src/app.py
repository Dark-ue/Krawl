import sys
import os
import tkinter as tk
from tkinter import ttk

# Add the 'src' directory to python path so it handles imports smoothly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from frontend.login import LoginFrame

class KrawlApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Krawl Portal")
        self.geometry("350x250")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        
        self.db_instance = None
        
        # Load the login window frame first
        self.current_frame = LoginFrame(self, on_success_callback=self.login_successful)

    def login_successful(self, user_uuid, email):
        # 1. Destroy login screen
        self.current_frame.destroy()
        
        # 2. Instantly unlock the Database using the UUID from Supabase
        print(f"Authenticating database layer for UUID: {user_uuid}")
        self.db_instance = Database("app.db", user_uuid)
        
        # 3. Transition to main UI workspace
        self.show_main_dashboard(email)

    def show_main_dashboard(self, email):
        self.geometry("600x400")  # Resize window for workspace view
        
        self.current_frame = ttk.Frame(self, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.current_frame, text=f"Active Mesh Session: {email}", font=("Arial", 9, "italic")).pack(anchor=tk.W)
        ttk.Label(self.current_frame, text="KRAWL MESH PROTOCOL", font=("Arial", 16, "bold")).pack(pady=30)
        
        # Add your chat/app elements here and pass self.db_instance to execute SQL tasks!
        ttk.Label(self.current_frame, text="🔒 Database: Active, Unlocked, & Sandboxed").pack(pady=10)

if __name__ == "__main__":
    app = KrawlApplication()
    app.mainloop()