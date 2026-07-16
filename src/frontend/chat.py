import subprocess
import platform
import tkinter as tk
from tkinter import messagebox, ttk
from backend.contact import Contact_imp

class ContactWindow(tk.Toplevel):
    def __init__(self, parent, db_instance):
        super().__init__(parent)
        self.parent = parent
        self.db = db_instance  # Unlocked local SQLCipher db instance
        
        self.title("Add Contact")
        self.geometry("320x220")
        self.resizable(False, False)
        
        # Lock focus to this window modal style
        self.transient(parent)
        self.grab_set()
        
        self.contact_ui()

    def contact_ui(self):
        ttk.Label(self, text="ADD MESH PEER", font=("Arial", 12, "bold")).pack(pady=10)

        ttk.Label(self, text="Peer Email Address:").pack(anchor=tk.W, padx=20, pady=(5, 0))
        self.email_entry = ttk.Entry(self, width=35)
        self.email_entry.pack(padx=20, pady=5)

        self.save_btn = ttk.Button(self, text="Fetch, Ping & Save", command=self.process_contact)
        self.save_btn.pack(pady=20, padx=20, fill=tk.X)

    def ping_ip(self, ip):
        """Pings the target IP address to check mesh routing status."""
        # Determine operating system flags (-n for Windows, -c for Unix/Linux)
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', ip]
        
        try:
            # Run the command invisibly without popping up consoles
            result = subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=3)
            return "Active" if result.returncode == 0 else "Offline"
        except Exception:
            return "Offline"

    def process_contact(self):
        peer_email = self.email_entry.get().strip()
        
        if not peer_email:
            messagebox.showerror("Error", "Please type a peer email handle.")
            return
            
        self.save_btn.config(state=tk.DISABLED)
        
        # 1. Fetch IP from Supabase via shared client
        contact_lookup = Contact_imp(peer_email)
        peer_ip = contact_lookup.ip_back()
        
        if not peer_ip:
            messagebox.showerror("Not Found", f"No active endpoint found for '{peer_email}'.")
            self.save_btn.config(state=tk.NORMAL)
            return
            
        # 2. Ping the endpoint
        status = self.ping_ip(peer_ip)
        print(f"Network check complete for {peer_ip}. Node Status: {status}")
        
        # 3. Save into local encrypted storage layer
        success = self.db.add_contact(username=peer_email, ip_address=peer_ip)
        
        if success:
            messagebox.showinfo("Success", f"Saved {peer_email}!\nIP: {peer_ip}\nStatus: {status}")
            self.destroy()
        else:
            messagebox.showerror("Error", "Failed saving contact. It may already exist locally.")
            self.save_btn.config(state=tk.NORMAL)


class ChatDashboard(ttk.Frame):
    def __init__(self, parent, db_instance, email):
        super().__init__(parent, padding="20")
        self.parent = parent
        self.db = db_instance
        self.email = email
        
        self.pack(fill=tk.BOTH, expand=True)
        self.setup_dashboard_ui()

    def setup_dashboard_ui(self):
        ttk.Label(self, text=f"Active Mesh Session: {self.email}", font=("Arial", 9, "italic")).pack(anchor=tk.W)
        ttk.Label(self, text="KRAWL MESH PROTOCOL", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self, text="🔒 Database: Active, Unlocked, & Sandboxed").pack(pady=5)

        # Bottom alignment layout row pinned to floor
        bottom_bar = ttk.Frame(self)
        bottom_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        
        # ➕ Button placed strictly at the lower left
        add_contact_btn = ttk.Button(bottom_bar, text="➕ Add Contact", command=self.open_con)
        add_contact_btn.pack(side=tk.LEFT)

    def open_con(self):
        # Fire up the TopLevel modal window blueprint
        ContactWindow(self.parent, self.db)