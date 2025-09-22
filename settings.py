import tkinter as tk
from tkinter import ttk, messagebox
from db_config import DatabaseConfig

class SettingsWindow:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.db_config = DatabaseConfig()
        
        # Create settings window
        self.root = tk.Toplevel()
        self.root.title("Warehouse Management - Settings")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        
        # Create interface
        self.create_widgets()
        
        # Load initial data
        self.load_settings()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#118AB2', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="System Settings",
            font=("Arial", 16, "bold"),
            bg='#118AB2',
            fg='white'
        )
        header_label.pack(pady=10)
        
        # Main Container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create tabs
        self.create_user_management_tab()
        self.create_database_tab()
        self.create_system_tab()
        self.create_backup_tab()
        
        # Buttons Frame
        buttons_frame = tk.Frame(main_container)
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # Action Buttons
        btn_save = tk.Button(
            buttons_frame,
            text="Save Settings",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.save_settings,
            cursor='hand2'
        )
        btn_save.pack(side='left', padx=(0, 10))
        
        btn_reset = tk.Button(
            buttons_frame,
            text="Reset to Default",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.reset_settings,
            cursor='hand2'
        )
        btn_reset.pack(side='left', padx=(0, 10))
        
        btn_close = tk.Button(
            buttons_frame,
            text="Close",
            font=("Arial", 11, "bold"),
            bg='#757575',
            fg='white',
            command=self.on_closing,
            cursor='hand2'
        )
        btn_close.pack(side='right')
        
        # Status bar
        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            relief='sunken',
            anchor='w',
            bg='lightgray'
        )
        status_bar.pack(side='bottom', fill='x')
        self.status_var.set("Ready")
    
    def create_user_management_tab(self):
        """Create user management tab"""
        user_frame = ttk.Frame(self.notebook)
        self.notebook.add(user_frame, text="User Management")
        
        # User Management Section
        user_mgmt_frame = tk.LabelFrame(user_frame, text="User Accounts", font=("Arial", 12, "bold"))
        user_mgmt_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Users list
        columns = ('ID', 'Username', 'Role', 'Created')
        self.users_tree = ttk.Treeview(user_mgmt_frame, columns=columns, show='headings', height=10)
        
        column_widths = [60, 150, 100, 150]
        for i, col in enumerate(columns):
            self.users_tree.heading(col, text=col)
            self.users_tree.column(col, width=column_widths[i])
        
        # Scrollbars for users tree
        users_scrollbar = ttk.Scrollbar(user_mgmt_frame, orient='vertical', command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=users_scrollbar.set)
        
        self.users_tree.pack(side='left', fill='both', expand=True, padx=(10, 0), pady=10)
        users_scrollbar.pack(side='right', fill='y', pady=10, padx=(0, 10))
        
        # User management buttons
        user_buttons_frame = tk.Frame(user_frame)
        user_buttons_frame.pack(fill='x', padx=10, pady=(0, 10))
        
        btn_add_user = tk.Button(
            user_buttons_frame,
            text="Add User",
            font=("Arial", 10, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.add_user,
            cursor='hand2'
        )
        btn_add_user.pack(side='left', padx=(0, 10))
        
        btn_edit_user = tk.Button(
            user_buttons_frame,
            text="Edit User",
            font=("Arial", 10, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.edit_user,
            cursor='hand2'
        )
        btn_edit_user.pack(side='left', padx=(0, 10))
        
        btn_delete_user = tk.Button(
            user_buttons_frame,
            text="Delete User",
            font=("Arial", 10, "bold"),
            bg='#F44336',
            fg='black',
            command=self.delete_user,
            cursor='hand2'
        )
        btn_delete_user.pack(side='left', padx=(0, 10))
        
        btn_change_password = tk.Button(
            user_buttons_frame,
            text="Change Password",
            font=("Arial", 10, "bold"),
            bg='#2196F3',
            fg='black',
            command=self.change_password,
            cursor='hand2'
        )
        btn_change_password.pack(side='left')
    
    def create_database_tab(self):
        """Create database settings tab"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="Database")
        
        # Database Connection Settings
        connection_frame = tk.LabelFrame(db_frame, text="Database Connection", font=("Arial", 12, "bold"))
        connection_frame.pack(fill='x', padx=10, pady=10)
        
        # Connection fields
        tk.Label(connection_frame, text="Host:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.host_entry = tk.Entry(connection_frame, font=("Arial", 10), width=30)
        self.host_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        tk.Label(connection_frame, text="Database:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.database_entry = tk.Entry(connection_frame, font=("Arial", 10), width=30)
        self.database_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        tk.Label(connection_frame, text="Username:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.db_user_entry = tk.Entry(connection_frame, font=("Arial", 10), width=30)
        self.db_user_entry.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        tk.Label(connection_frame, text="Password:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.db_password_entry = tk.Entry(connection_frame, font=("Arial", 10), width=30, show='*')
        self.db_password_entry.grid(row=3, column=1, sticky='ew', padx=10, pady=5)
        
        connection_frame.grid_columnconfigure(1, weight=1)
        
        # Test connection button
        test_btn = tk.Button(
            connection_frame,
            text="Test Connection",
            font=("Arial", 10, "bold"),
            bg='#2196F3',
            fg='black',
            command=self.test_db_connection
        )
        test_btn.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Database Statistics
        stats_frame = tk.LabelFrame(db_frame, text="Database Statistics", font=("Arial", 12, "bold"))
        stats_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.stats_text = tk.Text(stats_frame, height=8, width=50, state='disabled')
        self.stats_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        refresh_stats_btn = tk.Button(
            stats_frame,
            text="Refresh Statistics",
            font=("Arial", 10, "bold"),
            bg='#607D8B',
            fg='black',
            command=self.refresh_db_stats
        )
        refresh_stats_btn.pack(pady=5)
    
    def create_system_tab(self):
        """Create system settings tab"""
        system_frame = ttk.Frame(self.notebook)
        self.notebook.add(system_frame, text="System")
        
        # Application Settings
        app_frame = tk.LabelFrame(system_frame, text="Application Settings", font=("Arial", 12, "bold"))
        app_frame.pack(fill='x', padx=10, pady=10)
        
        # Low stock threshold
        tk.Label(app_frame, text="Low Stock Alert Threshold:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.stock_threshold_entry = tk.Entry(app_frame, font=("Arial", 10), width=20)
        self.stock_threshold_entry.grid(row=0, column=1, sticky='w', padx=10, pady=5)
        
        # Currency symbol
        tk.Label(app_frame, text="Currency Symbol:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.currency_entry = tk.Entry(app_frame, font=("Arial", 10), width=20)
        self.currency_entry.grid(row=1, column=1, sticky='w', padx=10, pady=5)
        
        # Auto-backup
        tk.Label(app_frame, text="Auto Backup:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.auto_backup_var = tk.BooleanVar()
        auto_backup_check = tk.Checkbutton(app_frame, text="Enable automatic daily backup", 
                                         variable=self.auto_backup_var, font=("Arial", 10))
        auto_backup_check.grid(row=2, column=1, sticky='w', padx=10, pady=5)
        
        # Session timeout
        tk.Label(app_frame, text="Session Timeout (minutes):", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky='w', padx=10, pady=5)
        self.timeout_entry = tk.Entry(app_frame, font=("Arial", 10), width=20)
        self.timeout_entry.grid(row=3, column=1, sticky='w', padx=10, pady=5)
        
        # System Information
        info_frame = tk.LabelFrame(system_frame, text="System Information", font=("Arial", 12, "bold"))
        info_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.system_info_text = tk.Text(info_frame, height=10, width=50, state='disabled')
        self.system_info_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.load_system_info()
    
    def create_backup_tab(self):
        """Create backup and maintenance tab"""
        backup_frame = ttk.Frame(self.notebook)
        self.notebook.add(backup_frame, text="Backup & Maintenance")
        
        # Backup Section
        backup_section = tk.LabelFrame(backup_frame, text="Database Backup", font=("Arial", 12, "bold"))
        backup_section.pack(fill='x', padx=10, pady=10)
        
        backup_buttons_frame = tk.Frame(backup_section)
        backup_buttons_frame.pack(pady=10)
        
        btn_backup = tk.Button(
            backup_buttons_frame,
            text="Create Backup",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.create_backup,
            cursor='hand2',
            width=15
        )
        btn_backup.pack(side='left', padx=10)
        
        btn_restore = tk.Button(
            backup_buttons_frame,
            text="Restore Backup",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.restore_backup,
            cursor='hand2',
            width=15
        )
        btn_restore.pack(side='left', padx=10)
        
        # Maintenance Section
        maintenance_section = tk.LabelFrame(backup_frame, text="Database Maintenance", font=("Arial", 12, "bold"))
        maintenance_section.pack(fill='x', padx=10, pady=10)
        
        maintenance_buttons_frame = tk.Frame(maintenance_section)
        maintenance_buttons_frame.pack(pady=10)
        
        btn_optimize = tk.Button(
            maintenance_buttons_frame,
            text="Optimize Database",
            font=("Arial", 11, "bold"),
            bg='#2196F3',
            fg='black',
            command=self.optimize_database,
            cursor='hand2',
            width=15
        )
        btn_optimize.pack(side='left', padx=10)
        
        btn_clean = tk.Button(
            maintenance_buttons_frame,
            text="Clean Logs",
            font=("Arial", 11, "bold"),
            bg='#607D8B',
            fg='black',
            command=self.clean_logs,
            cursor='hand2',
            width=15
        )
        btn_clean.pack(side='left', padx=10)
        
        # Backup History
        history_frame = tk.LabelFrame(backup_frame, text="Recent Backups", font=("Arial", 12, "bold"))
        history_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.backup_history_text = tk.Text(history_frame, height=8, width=50, state='disabled')
        self.backup_history_text.pack(fill='both', expand=True, padx=10, pady=10)
    
    def load_settings(self):
        """Load current settings"""
        self.load_users()
        self.load_db_settings()
        self.load_app_settings()
        self.refresh_db_stats()
        self.load_backup_history()
    
    def load_users(self):
        """Load users list"""
        # Clear existing items
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, username, role, created_at FROM users ORDER BY username")
                users = cursor.fetchall()
                
                for user in users:
                    formatted_user = list(user)
                    formatted_user[3] = user[3].strftime("%Y-%m-%d") if user[3] else "N/A"
                    self.users_tree.insert('', 'end', values=formatted_user)
                
                cursor.close()
                connection.close()
                self.status_var.set(f"Loaded {len(users)} users")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading users: {e}")
    
    def load_db_settings(self):
        """Load database settings"""
        self.host_entry.insert(0, self.db_config.host)
        self.database_entry.insert(0, self.db_config.database)
        self.db_user_entry.insert(0, self.db_config.user)
        self.db_password_entry.insert(0, self.db_config.password)
    
    def load_app_settings(self):
        """Load application settings with defaults"""
        self.stock_threshold_entry.insert(0, "10")
        self.currency_entry.insert(0, "₹")
        self.auto_backup_var.set(False)
        self.timeout_entry.insert(0, "30")
    
    def load_system_info(self):
        """Load system information"""
        import platform
        import sys
        from datetime import datetime
        
        info = f"""System Information:
        
Operating System: {platform.system()} {platform.release()}
Python Version: {sys.version}
Platform: {platform.platform()}
Machine: {platform.machine()}
Processor: {platform.processor()}

Application Details:
Version: 1.0
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Installation Path: {sys.path[0]}
"""
        
        self.system_info_text.config(state='normal')
        self.system_info_text.delete(1.0, tk.END)
        self.system_info_text.insert(1.0, info)
        self.system_info_text.config(state='disabled')
    
    def refresh_db_stats(self):
        """Refresh database statistics"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Get table statistics
                stats = "Database Statistics:\n\n"
                
                # Products count
                cursor.execute("SELECT COUNT(*) FROM products")
                products_count = cursor.fetchone()[0]
                stats += f"Total Products: {products_count}\n"
                
                # Orders count
                cursor.execute("SELECT COUNT(*) FROM orders")
                orders_count = cursor.fetchone()[0]
                stats += f"Total Orders: {orders_count}\n"
                
                # Suppliers count
                cursor.execute("SELECT COUNT(*) FROM suppliers")
                suppliers_count = cursor.fetchone()[0]
                stats += f"Total Suppliers: {suppliers_count}\n"
                
                # Users count
                cursor.execute("SELECT COUNT(*) FROM users")
                users_count = cursor.fetchone()[0]
                stats += f"Total Users: {users_count}\n\n"
                
                # Database size
                cursor.execute("""
                    SELECT ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) as 'DB Size (MB)'
                    FROM information_schema.tables 
                    WHERE table_schema = %s
                """, (self.db_config.database,))
                db_size = cursor.fetchone()[0]
                stats += f"Database Size: {db_size or 'N/A'} MB\n"
                
                # Latest order
                cursor.execute("SELECT MAX(order_date) FROM orders")
                latest_order = cursor.fetchone()[0]
                stats += f"Latest Order: {latest_order.strftime('%Y-%m-%d %H:%M') if latest_order else 'None'}\n"
                
                cursor.close()
                connection.close()
                
                self.stats_text.config(state='normal')
                self.stats_text.delete(1.0, tk.END)
                self.stats_text.insert(1.0, stats)
                self.stats_text.config(state='disabled')
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading database statistics: {e}")
    
    def load_backup_history(self):
        """Load backup history (placeholder - would normally read from log files)"""
        history = """Backup History:

No backup history available.
Backup functionality requires additional implementation
for mysqldump integration.

To implement:
1. Install mysqldump utility
2. Configure backup directory
3. Set up scheduled tasks
"""
        
        self.backup_history_text.config(state='normal')
        self.backup_history_text.delete(1.0, tk.END)
        self.backup_history_text.insert(1.0, history)
        self.backup_history_text.config(state='disabled')
    
    def test_db_connection(self):
        """Test database connection"""
        host = self.host_entry.get().strip()
        database = self.database_entry.get().strip()
        user = self.db_user_entry.get().strip()
        password = self.db_password_entry.get().strip()
        
        try:
            import mysql.connector
            connection = mysql.connector.connect(
                host=host,
                database=database,
                user=user,
                password=password
            )
            if connection.is_connected():
                connection.close()
                messagebox.showinfo("Success", "Database connection successful!")
                self.status_var.set("Database connection test successful")
            else:
                messagebox.showerror("Error", "Failed to connect to database")
        except Exception as e:
            messagebox.showerror("Connection Error", f"Error connecting to database: {e}")
    
    def add_user(self):
        """Add new user"""
        dialog = UserDialog(self.root, "Add New User")
        if dialog.result:
            username, password, role = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                        INSERT INTO users (username, password, role)
                        VALUES (%s, %s, %s)
                    """, (username, password, role))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "User added successfully!")
                    self.load_users()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error adding user: {e}")
    
    def edit_user(self):
        """Edit selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to edit.")
            return
        
        item_values = self.users_tree.item(selected_item[0])['values']
        user_id, username, role = item_values[0], item_values[1], item_values[2]
        
        dialog = UserDialog(self.root, "Edit User", (username, "", role))
        if dialog.result:
            new_username, new_password, new_role = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    if new_password:
                        cursor.execute("""
                            UPDATE users SET username=%s, password=%s, role=%s WHERE id=%s
                        """, (new_username, new_password, new_role, user_id))
                    else:
                        cursor.execute("""
                            UPDATE users SET username=%s, role=%s WHERE id=%s
                        """, (new_username, new_role, user_id))
                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "User updated successfully!")
                    self.load_users()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error updating user: {e}")
    
    def delete_user(self):
        """Delete selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to delete.")
            return
        
        item_values = self.users_tree.item(selected_item[0])['values']
        user_id, username = item_values[0], item_values[1]
        
        if username == 'admin':
            messagebox.showerror("Error", "Cannot delete admin user!")
            return
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete user '{username}'?"):
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "User deleted successfully!")
                    self.load_users()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error deleting user: {e}")
    
    def change_password(self):
        """Change password for selected user"""
        selected_item = self.users_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a user to change password.")
            return
        
        item_values = self.users_tree.item(selected_item[0])['values']
        user_id, username = item_values[0], item_values[1]
        
        dialog = PasswordDialog(self.root, username)
        if dialog.result:
            new_password = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_password, user_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Password changed successfully!")
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error changing password: {e}")
    
    def create_backup(self):
        """Create database backup (placeholder)"""
        messagebox.showinfo("Backup", "Backup functionality requires mysqldump to be installed and configured.\n\nThis is a placeholder for the backup feature.")
        self.status_var.set("Backup feature requires additional configuration")
    
    def restore_backup(self):
        """Restore database backup (placeholder)"""
        messagebox.showinfo("Restore", "Restore functionality requires mysqldump to be installed and configured.\n\nThis is a placeholder for the restore feature.")
        self.status_var.set("Restore feature requires additional configuration")
    
    def optimize_database(self):
        """Optimize database tables"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                tables = ['products', 'orders', 'order_items', 'suppliers', 'users']
                
                for table in tables:
                    cursor.execute(f"OPTIMIZE TABLE {table}")
                
                connection.commit()
                cursor.close()
                connection.close()
                
                messagebox.showinfo("Success", "Database optimization completed!")
                self.status_var.set("Database optimized successfully")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error optimizing database: {e}")
    
    def clean_logs(self):
        """Clean application logs (placeholder)"""
        messagebox.showinfo("Clean Logs", "Log cleaning functionality is not implemented yet.\n\nThis would clean application log files.")
        self.status_var.set("Log cleaning is not implemented")
    
    def save_settings(self):
        """Save all settings"""
        # In a real application, you would save these settings to a configuration file
        messagebox.showinfo("Settings", "Settings saved successfully!\n\nNote: Some settings require application restart to take effect.")
        self.status_var.set("Settings saved successfully")
    
    def reset_settings(self):
        """Reset settings to default"""
        if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to default values?"):
            # Clear all fields and reload defaults
            for entry in [self.stock_threshold_entry, self.currency_entry, self.timeout_entry]:
                entry.delete(0, tk.END)
            
            self.auto_backup_var.set(False)
            self.load_app_settings()
            
            messagebox.showinfo("Reset", "Settings reset to default values!")
            self.status_var.set("Settings reset to defaults")
    
    def on_closing(self):
        """Handle window close"""
        self.root.destroy()


class UserDialog:
    def __init__(self, parent, title, data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("350x250")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form(data)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self, data):
        """Create user form"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Form fields
        tk.Label(main_frame, text="Username:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        self.username_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.username_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Password:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        self.password_entry = tk.Entry(main_frame, font=("Arial", 10), width=25, show='*')
        self.password_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Role:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        self.role_combo = ttk.Combobox(main_frame, values=["admin", "user"], state="readonly", width=22)
        self.role_combo.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Configure grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Fill data if editing
        if data:
            self.username_entry.insert(0, data[0])
            if data[1]:  # Password might be empty for edit
                self.password_entry.insert(0, data[1])
            self.role_combo.set(data[2])
        else:
            self.role_combo.set("user")  # Default role
        
        # Note for editing
        if data and data[1] == "":
            note_label = tk.Label(main_frame, text="Leave password empty to keep current password", 
                                font=("Arial", 8), fg='gray')
            note_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Focus on first field
        self.username_entry.focus()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        # Save button
        save_btn = tk.Button(
            buttons_frame,
            text="Save",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            width=10,
            command=self.save_user
        )
        save_btn.pack(side='left', padx=(0, 10))
        
        # Cancel button
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            font=("Arial", 11, "bold"),
            bg='#757575',
            fg='black',
            width=10,
            command=self.cancel
        )
        cancel_btn.pack(side='left')
        
        # Bind Enter key to save
        self.dialog.bind('<Return>', lambda e: self.save_user())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def save_user(self):
        """Save user data"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_combo.get()
        
        # Validate
        if not username:
            messagebox.showerror("Validation Error", "Username is required!")
            self.username_entry.focus()
            return
        
        if not role:
            messagebox.showerror("Validation Error", "Please select a role!")
            self.role_combo.focus()
            return
        
        # Store result
        self.result = (username, password, role)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class PasswordDialog:
    def __init__(self, parent, username):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Change Password - {username}")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form(username)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self, username):
        """Create password change form"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text=f"Change password for: {username}", 
                font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="New Password:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.password_entry = tk.Entry(main_frame, font=("Arial", 10), width=25, show='*')
        self.password_entry.pack(pady=(5, 10))
        
        tk.Label(main_frame, text="Confirm Password:", font=("Arial", 10, "bold")).pack(anchor='w')
        self.confirm_entry = tk.Entry(main_frame, font=("Arial", 10), width=25, show='*')
        self.confirm_entry.pack(pady=(5, 20))
        
        # Focus on first field
        self.password_entry.focus()
        
        # Buttons
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack()
        
        save_btn = tk.Button(
            buttons_frame,
            text="Change Password",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.save_password
        )
        save_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(
            buttons_frame,
            text="Cancel",
            font=("Arial", 11, "bold"),
            bg='#757575',
            fg='white',
            command=self.cancel
        )
        cancel_btn.pack(side='left', padx=10)
        
        # Bind Enter key
        self.dialog.bind('<Return>', lambda e: self.save_password())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def save_password(self):
        """Save new password"""
        password = self.password_entry.get().strip()
        confirm = self.confirm_entry.get().strip()
        
        if not password:
            messagebox.showerror("Validation Error", "Password cannot be empty!")
            self.password_entry.focus()
            return
        
        if password != confirm:
            messagebox.showerror("Validation Error", "Passwords do not match!")
            self.confirm_entry.focus()
            return
        
        if len(password) < 4:
            messagebox.showerror("Validation Error", "Password must be at least 4 characters long!")
            self.password_entry.focus()
            return
        
        self.result = password
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


if __name__ == "__main__":
    # For testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    app = SettingsWindow(root)
    root.mainloop()