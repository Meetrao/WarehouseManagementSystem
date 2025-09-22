import tkinter as tk
from tkinter import messagebox
import sys

class DashboardWindow:
    def __init__(self, user_data):
        self.user_data = user_data  # (id, username, role)
        self.root = tk.Tk()
        self.root.title(f"Warehouse Dashboard - Welcome {user_data[1]}")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Create dashboard interface
        self.create_widgets()
        
        # Handle window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start the dashboard
        self.root.mainloop()
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Create and arrange all dashboard widgets"""
        # Header frame
        header_frame = tk.Frame(self.root, bg='#2E8B57', height=100)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        # Welcome message
        welcome_label = tk.Label(
            header_frame,
            text=f"Welcome to Warehouse Management System",
            font=("Arial", 18, "bold"),
            bg='#2E8B57',
            fg='white'
        )
        welcome_label.pack(pady=20)
        
        # User info
        user_info_label = tk.Label(
            header_frame,
            text=f"Logged in as: {self.user_data[1]} ({self.user_data[2]})",
            font=("Arial", 12),
            bg='#2E8B57',
            fg='lightgray'
        )
        user_info_label.pack()
        
        # Main content frame
        main_frame = tk.Frame(self.root, bg='lightgray', padx=40, pady=40)
        main_frame.pack(fill='both', expand=True)
        
        # Create button grid
        buttons_frame = tk.Frame(main_frame, bg='lightgray')
        buttons_frame.pack(expand=True)
        
        # Define button configurations
        buttons = [
            ("Manage Products", self.manage_products, "#FF6B35", 0, 0),
            ("Manage Orders", self.manage_orders, "#F7931E", 0, 1),
            ("Manage Suppliers", self.manage_suppliers, "#FFD23F", 1, 0),
            ("View Reports", self.view_reports, "#06FFA5", 1, 1),
            ("Settings", self.settings, "#118AB2", 2, 0),
            ("Logout", self.logout, "#EE6C4D", 2, 1)
        ]
        
        # Create buttons
        for text, command, color, row, col in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                font=("Arial", 14, "bold"),
                bg=color,
                fg='black',
                width=15,
                height=3,
                command=command,
                relief='raised',
                bd=3,
                cursor='hand2'
            )
            btn.grid(row=row, column=col, padx=15, pady=15, sticky='nsew')
            
            # Add hover effects
            self.add_hover_effect(btn, color)
        
        # Configure grid weights for responsive design
        for i in range(3):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(2):
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg='#2E8B57', height=30)
        footer_frame.pack(fill='x')
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="© 2024 Warehouse Management System | Version 1.0",
            font=("Arial", 9),
            bg='#2E8B57',
            fg='lightgray'
        )
        footer_label.pack(pady=5)
    
    def add_hover_effect(self, button, original_color):
        """Add hover effect to buttons"""
        def on_enter(e):
            button.config(bg=self.darken_color(original_color))
        
        def on_leave(e):
            button.config(bg=original_color)
        
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
    
    def darken_color(self, color):
        """Darken a hex color for hover effect"""
        # Simple color darkening - remove first character and replace with darker variant
        color_map = {
            "#FF6B35": "#E55A2B",
            "#F7931E": "#DD7F1A",
            "#FFD23F": "#E5BE35",
            "#06FFA5": "#05E594",
            "#118AB2": "#0F7BA0",
            "#EE6C4D": "#D45B43"
        }
        return color_map.get(color, color)
    
    def manage_products(self):
        """Handle Manage Products button click"""
        try:
            from products import ProductsWindow
            ProductsWindow(self.root)
        except ImportError:
            messagebox.showerror("Error", "Products module not found. Please ensure products.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening products window: {e}")
    
    def manage_orders(self):
        """Handle Manage Orders button click"""
        try:
            from orders import OrdersWindow
            OrdersWindow(self.root)
        except ImportError:
            messagebox.showerror("Error", "Orders module not found. Please ensure orders.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening orders window: {e}")
    
    def manage_suppliers(self):
        """Handle Manage Suppliers button click"""
        try:
            from suppliers import SuppliersWindow
            SuppliersWindow(self.root)
        except ImportError:
            messagebox.showerror("Error", "Suppliers module not found. Please ensure suppliers.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening suppliers window: {e}")
    
    def view_reports(self):
        """Handle View Reports button click"""
        try:
            from reports import ReportsWindow
            ReportsWindow(self.root)
        except ImportError as e:
            if "matplotlib" in str(e):
                messagebox.showerror("Missing Dependency", 
                                   "Reports module requires matplotlib.\n\nPlease install it with:\npip install matplotlib")
            else:
                messagebox.showerror("Error", "Reports module not found. Please ensure reports.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening reports window: {e}")
    
    def settings(self):
        """Handle Settings button click"""
        try:
            from settings import SettingsWindow
            SettingsWindow(self.root)
        except ImportError:
            messagebox.showerror("Error", "Settings module not found. Please ensure settings.py is in the same directory.")
        except Exception as e:
            messagebox.showerror("Error", f"Error opening settings window: {e}")
    
    def logout(self):
        """Handle logout"""
        result = messagebox.askyesno(
            "Logout", 
            f"Are you sure you want to logout, {self.user_data[1]}?"
        )
        if result:
            self.root.destroy()
            # Restart the application by importing and running login
            from login import LoginWindow
            login_app = LoginWindow()
            login_app.run()
    
    def on_closing(self):
        """Handle window close event"""
        result = messagebox.askyesno(
            "Exit Application",
            "Are you sure you want to exit the Warehouse Management System?"
        )
        if result:
            self.root.destroy()
            sys.exit()

if __name__ == "__main__":
    # For testing purposes - normally called from login
    test_user = (1, "admin", "admin")
    app = DashboardWindow(test_user)