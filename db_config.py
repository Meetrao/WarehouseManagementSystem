import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox

class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'
        self.database = 'warehouse_db'
        self.user = 'root'
        self.password = '9325473165'  # Replace with your MySQL root password
    
    def get_connection(self):
        """Create and return a database connection"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                autocommit=False
            )
            if connection.is_connected():
                return connection
        except Error as e:
            self.handle_connection_error(e)
            return None
    
    def handle_connection_error(self, error):
        """Handle database connection errors with user-friendly messages"""
        error_code = error.errno if hasattr(error, 'errno') else None
        
        if error_code == 1049:  # Database doesn't exist
            messagebox.showerror(
                "Database Error",
                f"Database '{self.database}' does not exist!\n\n"
                "Please run the database_setup.sql script first to create the database and tables.\n\n"
                "Steps:\n"
                "1. Open MySQL command line or MySQL Workbench\n"
                "2. Run the database_setup.sql script\n"
                "3. Restart the application"
            )
        elif error_code == 1045:  # Access denied
            messagebox.showerror(
                "Database Error",
                f"Access denied for user '{self.user}'!\n\n"
                "Please check your MySQL credentials in db_config.py:\n"
                f"- Username: {self.user}\n"
                f"- Password: {'*' * len(self.password)}\n"
                f"- Host: {self.host}"
            )
        elif error_code == 2003:  # Can't connect to MySQL server
            messagebox.showerror(
                "Database Error",
                f"Cannot connect to MySQL server at '{self.host}'!\n\n"
                "Please ensure:\n"
                "1. MySQL server is running\n"
                "2. Host address is correct\n"
                "3. Port 3306 is accessible"
            )
        elif error_code == 1146:  # Table doesn't exist
            messagebox.showerror(
                "Database Error",
                "Required database tables are missing!\n\n"
                "Please run the database_setup.sql script to create all required tables.\n\n"
                "The script will create:\n"
                "- users table\n"
                "- products table\n"
                "- suppliers table\n"
                "- orders table\n"
                "- order_items table"
            )
        else:
            messagebox.showerror(
                "Database Error",
                f"Database connection failed!\n\n"
                f"Error: {error}\n\n"
                "Please check your database configuration and ensure MySQL server is running."
            )
        
        print(f"Database connection error: {error}")
    
    def verify_user(self, username, password):
        """Verify user credentials against database"""
        connection = self.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                query = "SELECT id, username, role FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (username, password))
                user = cursor.fetchone()
                cursor.close()
                connection.close()
                return user
            except Error as e:
                print(f"Error verifying user: {e}")
                if e.errno == 1146:  # Table doesn't exist
                    messagebox.showerror(
                        "Database Error",
                        "Users table does not exist!\n\n"
                        "Please run the database_setup.sql script to create the required tables."
                    )
                connection.close()
                return None
        return None
    
    def test_connection(self):
        """Test database connection and return result"""
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            if connection.is_connected():
                connection.close()
                return True, "Connection successful"
        except Error as e:
            return False, str(e)
        return False, "Unknown error"
    
    def check_tables_exist(self):
        """Check if all required tables exist"""
        required_tables = ['users', 'products', 'suppliers', 'orders', 'order_items']
        connection = self.get_connection()
        
        if not connection:
            return False, "Cannot connect to database"
        
        try:
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            missing_tables = [table for table in required_tables if table not in existing_tables]
            
            cursor.close()
            connection.close()
            
            if missing_tables:
                return False, f"Missing tables: {', '.join(missing_tables)}"
            else:
                return True, "All required tables exist"
                
        except Error as e:
            connection.close()
            return False, f"Error checking tables: {e}"