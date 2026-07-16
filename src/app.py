import sys
import os
import tkinter as tk
from tkinter import ttk
from backend.contact import Contact_imp
from frontend.chat import ChatDashboard

# Add the 'src' directory to python path so it handles imports smoothly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.database import Database
from frontend.login import LoginFrame

class KrawlApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Krawl Messenger")
        self.geometry("350x250")
        self.resizable(False, False)
        self.eval('tk::PlaceWindow . center')
        
        self.db_instance = None
        
        self.current_frame = LoginFrame(self, on_success_callback=self.login_successful)

    def login_successful(self, user_uuid, email):
       
        self.current_frame.destroy()
        
        print(f"Authenticating database layer for UUID: {user_uuid}")
        self.db_instance = Database("app.db", user_uuid)
        
        self.show_main_dashboard(email)

    def show_main_dashboard(self, email):
        self.geometry("600x400")  
        
        self.current_frame = ttk.Frame(self, padding="20")
        self.current_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(self.current_frame, text=f"Active Mesh Session: {email}", font=("Arial", 9, "italic")).pack(anchor=tk.W)
        ttk.Label(self.current_frame, text="KRAWL MESH PROTOCOL", font=("Arial", 16, "bold")).pack(pady=30)
        
        # Add your chat/app elements here and pass self.db_instance to execute SQL tasks!
        ttk.Label(self.current_frame, text="🔒 Database: Active, Unlocked, & Sandboxed").pack(pady=10)

    
    def show_main_dashboard(self, email):
        self.geometry("600x400")
        self.resizable(True, True)

        self.current_frame = ChatDashboard(self, self.db_instance, email)


if __name__ == "__main__":
    app = KrawlApplication()
    app.mainloop()

    contact = Contact_imp('admin@trinetra.self')
    ip = contact.ip_back()

    print(ip)