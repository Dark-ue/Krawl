import tkinter as tk
from tkinter import messagebox, ttk

class ContactWindow(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Contact")

        self.geometry("300x200")
        self.contact_ui()


    def contact_ui(self):
        ttk.Label(self, text="ADD CONTACT", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(self, text="Username:").pack(anchor=tk.W, pady=(5, 0))
        ttk.Entry(self)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")

        contact_btn = ttk.Button(self, text="Add Contact", command=self.open_con)
        contact_btn.pack(expand=True)

    def open_con(self):
        pass




if __name__=="__main__":
    app = MainWindow()
    app.mainloop()