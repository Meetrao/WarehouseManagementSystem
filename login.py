import tkinter as tk
from tkinter import messagebox, ttk
from db_config import DatabaseConfig
from dashboard import DashboardWindow

class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Warehouse Management System - Login")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Center the window
        self.center_window()
        
        # Database config
        self.db_config = DatabaseConfig()
        
        # Create login interface
        self.create_widgets()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Main frame
        main_frame = tk.Frame(self.root, bg='lightblue', padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Warehouse Management System", 
            font=("Arial", 16, "bold"),
            bg='lightblue'
        )
        title_label.pack(pady=(0, 30))
        
        # Login form frame
        form_frame = tk.Frame(main_frame, bg='white', padx=20, pady=20, relief='raised', bd=2)
        form_frame.pack()
        
        # Username
        tk.Label(form_frame, text="Username:", font=("Arial", 12), bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(form_frame, font=("Arial", 12), width=25)
        self.username_entry.pack(pady=(5, 15))
        self.username_entry.focus()  # Set focus on username field
        
        # Password
        tk.Label(form_frame, text="Password:", font=("Arial", 12), bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(form_frame, font=("Arial", 12), width=25, show='*')
        self.password_entry.pack(pady=(5, 20))
        
        # Login button
        login_btn = tk.Button(
            form_frame,
            text="Login",
            font=("Arial", 12, "bold"),
            bg='#4CAF50',
            fg='black',
            width=20,
            command=self.login
        )
        login_btn.pack(pady=(0, 10))
        
        # Demo credentials info
        info_frame = tk.Frame(main_frame, bg='lightblue')
        info_frame.pack(pady=(20, 0))
        
        tk.Label(
            info_frame,
            text="Demo Credentials:",
            font=("Arial", 10, "bold"),
            bg='lightblue'
        ).pack()
        
        tk.Label(
            info_frame,
            text="Username: admin | Password: admin123",
            font=("Arial", 9),
            bg='lightblue',
            fg='gray'
        ).pack()
        
        # Bind Enter key to login
        self.root.bind('<Return>', lambda event: self.login())
    
    def login(self):
        """Handle login process"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Validate input
        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password!")
            return
        
        # Verify credentials
        user = self.db_config.verify_user(username, password)
        
        if user:
            messagebox.showinfo("Success", f"Welcome, {user[1]}!")
            # Close login window
            self.root.destroy()
            # Open dashboard
            dashboard = DashboardWindow(user)
        else:
            messagebox.showerror("Error", "Invalid username or password!")
            self.password_entry.delete(0, tk.END)  # Clear password field
    
    def run(self):
        """Start the login window"""
        self.root.mainloop()

if __name__ == "__main__":
    app = LoginWindow()
    app.run()