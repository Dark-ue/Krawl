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
        """Mounts the primary chat dashboard view after successful authentication."""
        self.geometry("600x400")
        self.resizable(True, True)

        # Securely pass the application window reference, the unlocked db context, and the session email
        self.current_frame = ChatDashboard(self, self.db_instance, email)


if __name__ == "__main__":
    app = KrawlApplication()
    app.mainloop()