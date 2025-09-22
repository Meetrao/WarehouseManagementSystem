import tkinter as tk
from tkinter import ttk, messagebox
from db_config import DatabaseConfig

class ProductsWindow:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.db_config = DatabaseConfig()
        
        # Create products window
        self.root = tk.Toplevel()
        self.root.title("Warehouse Management - Products")
        self.root.geometry("900x500")
        self.root.resizable(True, True)
        
        # Create interface
        self.create_widgets()
        
        # Load initial data
        self.refresh_products()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#2E8B57', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Products Management",
            font=("Arial", 16, "bold"),
            bg='#2E8B57',
            fg='white'
        )
        header_label.pack(pady=10)
        
        # Main Container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Buttons Frame
        buttons_frame = tk.Frame(main_container)
        buttons_frame.pack(fill='x', pady=(0, 10))
        
        # Action Buttons
        btn_add = tk.Button(
            buttons_frame,
            text="Add New Product",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.add_product,
            cursor='hand2'
        )
        btn_add.pack(side='left', padx=(0, 10))
        
        btn_edit = tk.Button(
            buttons_frame,
            text="Edit Product",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.edit_product,
            cursor='hand2'
        )
        btn_edit.pack(side='left', padx=(0, 10))
        
        btn_delete = tk.Button(
            buttons_frame,
            text="Delete Product",
            font=("Arial", 11, "bold"),
            bg='#F44336',
            fg='black',
            command=self.delete_product,
            cursor='hand2'
        )
        btn_delete.pack(side='left', padx=(0, 10))
        
        btn_refresh = tk.Button(
            buttons_frame,
            text="Refresh",
            font=("Arial", 11, "bold"),
            bg='#2196F3',
            fg='black',
            command=self.refresh_products,
            cursor='hand2'
        )
        btn_refresh.pack(side='left', padx=(0, 10))
        
        # Search Frame (Simplified - No auto-search)
        search_frame = tk.Frame(buttons_frame)
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side='left', padx=(5, 5))
        
        search_btn = tk.Button(
            search_frame,
            text="Go",
            command=self.search_products,
            bg='#607D8B',
            fg='white'
        )
        search_btn.pack(side='left')
        
        # Products Table Frame
        table_frame = tk.Frame(main_container)
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview (Table)
        columns = ('ID', 'Name', 'Description', 'Price', 'Quantity', 'Category', 'Supplier')
        self.products_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = [50, 150, 200, 100, 80, 120, 150]
        for i, col in enumerate(columns):
            self.products_tree.heading(col, text=col)
            self.products_tree.column(col, width=column_widths[i], minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.products_tree.yview)
        self.products_tree.configure(yscrollcommand=v_scrollbar.set)
        
        # Pack table and scrollbars
        self.products_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Bind double-click to edit
        self.products_tree.bind('<Double-1>', lambda e: self.edit_product())
        
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
    
    def refresh_products(self):
        """Refresh the products table"""
        # Clear existing items
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        # Fetch products from database
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, name, description, price, quantity, category, supplier 
                    FROM products 
                    ORDER BY name
                """)
                products = cursor.fetchall()
                
                # Insert products into table
                for product in products:
                    # Format price with ₹ symbol
                    formatted_product = list(product)
                    formatted_product[3] = f"₹{product[3]:,.2f}"
                    self.products_tree.insert('', 'end', values=formatted_product)
                
                self.status_var.set(f"Loaded {len(products)} products")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading products: {e}")
                self.status_var.set("Error loading products")
    
    def add_product(self):
        """Add a new product"""
        dialog = ProductDialog(self.root, "Add New Product")
        if dialog.result:
            product_data = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    query = """
                        INSERT INTO products (name, description, price, quantity, category, supplier)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, product_data)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Product added successfully!")
                    self.refresh_products()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error adding product: {e}")
    
    def edit_product(self):
        """Edit selected product"""
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a product to edit.")
            return
        
        # Get product data
        item_values = self.products_tree.item(selected_item[0])['values']
        product_id = item_values[0]
        
        # Remove ₹ symbol and commas from price for editing
        price_str = str(item_values[3]).replace('₹', '').replace(',', '')
        
        # Prepare data for dialog
        current_data = (
            item_values[1],  # name
            item_values[2],  # description
            float(price_str),  # price
            int(item_values[4]),  # quantity
            item_values[5],  # category
            item_values[6]   # supplier
        )
        
        dialog = ProductDialog(self.root, "Edit Product", current_data)
        if dialog.result:
            product_data = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    query = """
                        UPDATE products 
                        SET name=%s, description=%s, price=%s, quantity=%s, category=%s, supplier=%s
                        WHERE id=%s
                    """
                    cursor.execute(query, product_data + (product_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Product updated successfully!")
                    self.refresh_products()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error updating product: {e}")
    
    def delete_product(self):
        """Delete selected product"""
        selected_item = self.products_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a product to delete.")
            return
        
        item_values = self.products_tree.item(selected_item[0])['values']
        product_id = item_values[0]
        product_name = item_values[1]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{product_name}'?"):
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM products WHERE id = %s", (product_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Product deleted successfully!")
                    self.refresh_products()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error deleting product: {e}")
    
    def search_products(self):
        """Search products by name - Manual search"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear and reload filtered data
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                if search_term:
                    query = """
                        SELECT id, name, description, price, quantity, category, supplier 
                        FROM products 
                        WHERE LOWER(name) LIKE %s OR LOWER(category) LIKE %s OR LOWER(supplier) LIKE %s
                        ORDER BY name
                    """
                    search_pattern = f"%{search_term}%"
                    cursor.execute(query, (search_pattern, search_pattern, search_pattern))
                else:
                    cursor.execute("""
                        SELECT id, name, description, price, quantity, category, supplier 
                        FROM products 
                        ORDER BY name
                    """)
                
                products = cursor.fetchall()
                
                for product in products:
                    formatted_product = list(product)
                    formatted_product[3] = f"₹{product[3]:,.2f}"
                    self.products_tree.insert('', 'end', values=formatted_product)
                
                self.status_var.set(f"Found {len(products)} products")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error searching products: {e}")
    
    def on_closing(self):
        """Handle window close"""
        self.root.destroy()


class ProductDialog:
    def __init__(self, parent, title, data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x320")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form(data)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self, data):
        """Create form fields"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Form fields
        tk.Label(main_frame, text="Product Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        self.name_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.name_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Description:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        self.desc_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.desc_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Price (₹):", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        self.price_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.price_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Quantity:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        self.quantity_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.quantity_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Category:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky='w', pady=5)
        self.category_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.category_entry.grid(row=4, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Supplier:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky='w', pady=5)
        self.supplier_entry = tk.Entry(main_frame, font=("Arial", 10), width=25)
        self.supplier_entry.grid(row=5, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Configure grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Fill data if editing
        if data:
            self.name_entry.insert(0, data[0])
            self.desc_entry.insert(0, data[1])
            self.price_entry.insert(0, str(data[2]))
            self.quantity_entry.insert(0, str(data[3]))
            self.category_entry.insert(0, data[4])
            self.supplier_entry.insert(0, data[5])
        
        # Focus on first field
        self.name_entry.focus()
        
        # Buttons frame
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        # Save button
        save_btn = tk.Button(
            buttons_frame,
            text="Save",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            width=10,
            command=self.save_product
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
        self.dialog.bind('<Return>', lambda e: self.save_product())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def save_product(self):
        """Save product data"""
        # Get values
        name = self.name_entry.get().strip()
        description = self.desc_entry.get().strip()
        price_str = self.price_entry.get().strip()
        quantity_str = self.quantity_entry.get().strip()
        category = self.category_entry.get().strip()
        supplier = self.supplier_entry.get().strip()
        
        # Validate
        if not name:
            messagebox.showerror("Validation Error", "Product name is required!")
            self.name_entry.focus()
            return
        
        try:
            price = float(price_str)
            if price < 0:
                raise ValueError("Price cannot be negative")
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid price!")
            self.price_entry.focus()
            return
        
        try:
            quantity = int(quantity_str)
            if quantity < 0:
                raise ValueError("Quantity cannot be negative")
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid quantity!")
            self.quantity_entry.focus()
            return
        
        # Store result
        self.result = (name, description, price, quantity, category, supplier)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()

if __name__ == "__main__":
    # For testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    app = ProductsWindow(root)
    root.mainloop()