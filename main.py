#!/usr/bin/env python3
"""
Warehouse Management System
Main application entry point

Author: Your Name
Date: 2024
Version: 1.0

This application provides a simple warehouse management interface with:
- User authentication
- Dashboard with management options
- MySQL database integration
"""

import sys
import tkinter as tk
from tkinter import messagebox
from login import LoginWindow

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import mysql.connector
        return True
    except ImportError as e:
        messagebox.showerror(
            "Missing Dependencies",
            f"Required module not found: {e}\n\n"
            "Please install missing dependencies:\n"
            "pip3 install mysql-connector-python"
        )
        return False

def main():
    """Main application function"""
    print("=" * 50)
    print("   WAREHOUSE MANAGEMENT SYSTEM")
    print("=" * 50)
    print("Starting application...")
    
    # Check dependencies
    if not check_dependencies():
        print("Error: Missing dependencies. Please install required modules.")
        sys.exit(1)
    
    try:
        # Create and run login window
        print("Initializing login window...")
        login_app = LoginWindow()
        login_app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        messagebox.showerror(
            "Application Error",
            f"An error occurred while starting the application:\n{e}\n\n"
            "Please check your database connection and try again."
        )
        sys.exit(1)

if __name__ == "__main__":
    main()