#!/usr/bin/env python3
"""
Database Setup Checker for Warehouse Management System

This script checks if the database and all required tables are properly set up.
Run this before running the main application to verify your database setup.
"""

import mysql.connector
from mysql.connector import Error
import sys

class DatabaseChecker:
    def __init__(self):
        # Database configuration - update these with your settings
        self.host = 'localhost'
        self.database = 'warehouse_db'
        self.user = 'root'
        self.password = '9325473165'  # Replace with your MySQL password
        
        self.required_tables = ['users', 'products', 'suppliers', 'orders', 'order_items']
        self.required_columns = {
            'users': ['id', 'username', 'password', 'role', 'created_at', 'updated_at'],
            'products': ['id', 'name', 'description', 'price', 'quantity', 'category', 'supplier', 'created_at', 'updated_at'],
            'suppliers': ['id', 'company_name', 'contact_person', 'phone', 'email', 'address', 'notes', 'created_at', 'updated_at'],
            'orders': ['id', 'customer_name', 'customer_phone', 'customer_address', 'total_amount', 'status', 'order_date', 'updated_at'],
            'order_items': ['id', 'order_id', 'product_id', 'quantity', 'unit_price', 'total_price', 'created_at']
        }
    
    def check_mysql_connection(self):
        """Test MySQL server connection"""
        print("1. Testing MySQL server connection...")
        try:
            # Try to connect without specifying database
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            if connection.is_connected():
                db_info = connection.get_server_info()
                print(f"   ✓ Connected to MySQL Server version {db_info}")
                connection.close()
                return True
            else:
                print("   ✗ Failed to connect to MySQL server")
                return False
                
        except Error as e:
            print(f"   ✗ MySQL connection failed: {e}")
            self.print_connection_help(e)
            return False
    
    def check_database_exists(self):
        """Check if the warehouse_db database exists"""
        print("\n2. Checking if warehouse_db database exists...")
        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            
            cursor = connection.cursor()
            cursor.execute("SHOW DATABASES")
            databases = [db[0] for db in cursor.fetchall()]
            
            if self.database in databases:
                print(f"   ✓ Database '{self.database}' exists")
                cursor.close()
                connection.close()
                return True
            else:
                print(f"   ✗ Database '{self.database}' does not exist")
                cursor.close()
                connection.close()
                return False
                
        except Error as e:
            print(f"   ✗ Error checking database: {e}")
            return False
    
    def check_tables_exist(self):
        """Check if all required tables exist"""
        print("\n3. Checking if all required tables exist...")
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            cursor = connection.cursor()
            cursor.execute("SHOW TABLES")
            existing_tables = [table[0] for table in cursor.fetchall()]
            
            all_tables_exist = True
            for table in self.required_tables:
                if table in existing_tables:
                    print(f"   ✓ Table '{table}' exists")
                else:
                    print(f"   ✗ Table '{table}' is missing")
                    all_tables_exist = False
            
            cursor.close()
            connection.close()
            return all_tables_exist
            
        except Error as e:
            print(f"   ✗ Error checking tables: {e}")
            return False
    
    def check_table_columns(self):
        """Check if all required columns exist in tables"""
        print("\n4. Checking table column structure...")
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            cursor = connection.cursor()
            all_columns_correct = True
            
            for table_name, required_cols in self.required_columns.items():
                cursor.execute(f"DESCRIBE {table_name}")
                existing_cols = [col[0] for col in cursor.fetchall()]
                
                print(f"   Table '{table_name}':")
                for col in required_cols:
                    if col in existing_cols:
                        print(f"     ✓ Column '{col}' exists")
                    else:
                        print(f"     ✗ Column '{col}' is missing")
                        all_columns_correct = False
            
            cursor.close()
            connection.close()
            return all_columns_correct
            
        except Error as e:
            print(f"   ✗ Error checking columns: {e}")
            return False
    
    def check_sample_data(self):
        """Check if sample data exists"""
        print("\n5. Checking for sample data...")
        try:
            connection = mysql.connector.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            
            cursor = connection.cursor()
            
            # Check admin user
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
            admin_count = cursor.fetchone()[0]
            
            if admin_count > 0:
                print("   ✓ Admin user exists")
            else:
                print("   ✗ Admin user is missing")
            
            # Check sample data counts
            for table in self.required_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   • {table}: {count} records")
            
            cursor.close()
            connection.close()
            return admin_count > 0
            
        except Error as e:
            print(f"   ✗ Error checking sample data: {e}")
            return False
    
    def print_connection_help(self, error):
        """Print helpful information for connection errors"""
        print("\n" + "="*50)
        print("CONNECTION TROUBLESHOOTING HELP")
        print("="*50)
        
        if error.errno == 1045:
            print("Access Denied Error:")
            print("- Check your MySQL username and password")
            print("- Make sure the user has proper privileges")
            print(f"- Current settings: host={self.host}, user={self.user}")
            
        elif error.errno == 2003:
            print("Can't Connect to Server:")
            print("- Make sure MySQL server is running")
            print("- Check if the host address is correct")
            print("- Verify that port 3306 is accessible")
            
        else:
            print(f"Error Code {error.errno}: {error}")
        
        print("\nTo fix these issues:")
        print("1. Update the credentials in this file and db_config.py")
        print("2. Ensure MySQL server is running")
        print("3. Run the database_setup.sql script")
    
    def print_setup_instructions(self):
        """Print database setup instructions"""
        print("\n" + "="*60)
        print("DATABASE SETUP INSTRUCTIONS")
        print("="*60)
        print("To set up your database properly, follow these steps:")
        print()
        print("1. Make sure MySQL server is installed and running")
        print("2. Open MySQL command line or MySQL Workbench")
        print("3. Run the database_setup.sql script:")
        print("   mysql -u root -p < database_setup.sql")
        print("4. Or copy and paste the SQL commands from database_setup.sql")
        print("5. Update the password in db_config.py to match your MySQL root password")
        print("6. Run this checker again to verify setup")
        print()
        print("If you continue to have issues:")
        print("- Check MySQL server status")
        print("- Verify user credentials")
        print("- Ensure all tables are created with correct structure")
    
    def run_all_checks(self):
        """Run all database checks"""
        print("WAREHOUSE MANAGEMENT SYSTEM - DATABASE SETUP CHECKER")
        print("="*60)
        
        checks = [
            self.check_mysql_connection(),
            self.check_database_exists(),
            self.check_tables_exist(),
            self.check_table_columns(),
            self.check_sample_data()
        ]
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        if all(checks):
            print("🎉 All checks passed! Your database is properly set up.")
            print("You can now run the Warehouse Management System application.")
        else:
            print("❌ Some checks failed. Please fix the issues above.")
            self.print_setup_instructions()
        
        return all(checks)

def main():
    """Main function"""
    checker = DatabaseChecker()
    
    try:
        success = checker.run_all_checks()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n\nSetup check interrupted by user.")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()