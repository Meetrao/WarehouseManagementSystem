import tkinter as tk
from tkinter import ttk, messagebox
from db_config import DatabaseConfig

class SuppliersWindow:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.db_config = DatabaseConfig()
        
        # Create suppliers window
        self.root = tk.Toplevel()
        self.root.title("Warehouse Management - Suppliers")
        self.root.geometry("900x500")
        self.root.resizable(True, True)
        
        # Create interface
        self.create_widgets()
        
        # Load initial data
        self.refresh_suppliers()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#FFD23F', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Suppliers Management",
            font=("Arial", 16, "bold"),
            bg='#FFD23F',
            fg='black'
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
            text="Add New Supplier",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.add_supplier,
            cursor='hand2'
        )
        btn_add.pack(side='left', padx=(0, 10))
        
        btn_edit = tk.Button(
            buttons_frame,
            text="Edit Supplier",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.edit_supplier,
            cursor='hand2'
        )
        btn_edit.pack(side='left', padx=(0, 10))
        
        btn_delete = tk.Button(
            buttons_frame,
            text="Delete Supplier",
            font=("Arial", 11, "bold"),
            bg='#F44336',
            fg='black',
            command=self.delete_supplier,
            cursor='hand2'
        )
        btn_delete.pack(side='left', padx=(0, 10))
        
        btn_view_products = tk.Button(
            buttons_frame,
            text="View Products",
            font=("Arial", 11, "bold"),
            bg='#9C27B0',
            fg='black',
            command=self.view_supplier_products,
            cursor='hand2'
        )
        btn_view_products.pack(side='left', padx=(0, 10))
        
        btn_refresh = tk.Button(
            buttons_frame,
            text="Refresh",
            font=("Arial", 11, "bold"),
            bg='#607D8B',
            fg='black',
            command=self.refresh_suppliers,
            cursor='hand2'
        )
        btn_refresh.pack(side='left', padx=(0, 10))
        
        # Search Frame
        search_frame = tk.Frame(buttons_frame)
        search_frame.pack(side='right')
        
        tk.Label(search_frame, text="Search:", font=("Arial", 10)).pack(side='left')
        self.search_entry = tk.Entry(search_frame, width=20)
        self.search_entry.pack(side='left', padx=(5, 5))
        
        search_btn = tk.Button(
            search_frame,
            text="Go",
            command=self.search_suppliers,
            bg='#607D8B',
            fg='white'
        )
        search_btn.pack(side='left')
        
        # Suppliers Table Frame
        table_frame = tk.Frame(main_container)
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview (Table)
        columns = ('ID', 'Company Name', 'Contact Person', 'Phone', 'Email', 'Address', 'Products Count')
        self.suppliers_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # Define column headings and widths
        column_widths = [50, 150, 120, 120, 150, 200, 100]
        for i, col in enumerate(columns):
            self.suppliers_tree.heading(col, text=col)
            self.suppliers_tree.column(col, width=column_widths[i], minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.suppliers_tree.yview)
        self.suppliers_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.suppliers_tree.xview)
        self.suppliers_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.suppliers_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click to edit
        self.suppliers_tree.bind('<Double-1>', lambda e: self.edit_supplier())
        
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
    
    def refresh_suppliers(self):
        """Refresh the suppliers table"""
        # Clear existing items
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Fetch suppliers from database
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT s.id, s.company_name, s.contact_person, s.phone, s.email, s.address,
                           COUNT(p.id) as product_count
                    FROM suppliers s
                    LEFT JOIN products p ON s.company_name = p.supplier
                    GROUP BY s.id, s.company_name, s.contact_person, s.phone, s.email, s.address
                    ORDER BY s.company_name
                """)
                suppliers = cursor.fetchall()
                
                # Insert suppliers into table
                for supplier in suppliers:
                    self.suppliers_tree.insert('', 'end', values=supplier)
                
                self.status_var.set(f"Loaded {len(suppliers)} suppliers")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading suppliers: {e}")
                self.status_var.set("Error loading suppliers")
    
    def add_supplier(self):
        """Add a new supplier"""
        dialog = SupplierDialog(self.root, "Add New Supplier")
        if dialog.result:
            supplier_data = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    query = """
                        INSERT INTO suppliers (company_name, contact_person, phone, email, address, notes)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(query, supplier_data)
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Supplier added successfully!")
                    self.refresh_suppliers()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error adding supplier: {e}")
    
    def edit_supplier(self):
        """Edit selected supplier"""
        selected_item = self.suppliers_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a supplier to edit.")
            return
        
        # Get supplier data
        item_values = self.suppliers_tree.item(selected_item[0])['values']
        supplier_id = item_values[0]
        
        # Get full supplier data from database
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT company_name, contact_person, phone, email, address, notes
                    FROM suppliers WHERE id = %s
                """, (supplier_id,))
                current_data = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if current_data:
                    dialog = SupplierDialog(self.root, "Edit Supplier", current_data)
                    if dialog.result:
                        supplier_data = dialog.result
                        connection = self.db_config.get_connection()
                        if connection:
                            try:
                                cursor = connection.cursor()
                                query = """
                                    UPDATE suppliers 
                                    SET company_name=%s, contact_person=%s, phone=%s, email=%s, address=%s, notes=%s
                                    WHERE id=%s
                                """
                                cursor.execute(query, supplier_data + (supplier_id,))
                                connection.commit()
                                cursor.close()
                                connection.close()
                                
                                messagebox.showinfo("Success", "Supplier updated successfully!")
                                self.refresh_suppliers()
                                
                            except Exception as e:
                                messagebox.showerror("Database Error", f"Error updating supplier: {e}")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading supplier data: {e}")
    
    def delete_supplier(self):
        """Delete selected supplier"""
        selected_item = self.suppliers_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a supplier to delete.")
            return
        
        item_values = self.suppliers_tree.item(selected_item[0])['values']
        supplier_id = item_values[0]
        company_name = item_values[1]
        product_count = item_values[6]
        
        # Check if supplier has products
        if product_count > 0:
            result = messagebox.askyesno(
                "Products Found", 
                f"This supplier has {product_count} products associated with it.\n"
                f"Are you sure you want to delete '{company_name}'?\n\n"
                f"Note: This will not delete the products, but will remove the supplier reference."
            )
        else:
            result = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{company_name}'?")
        
        if result:
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("DELETE FROM suppliers WHERE id = %s", (supplier_id,))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Supplier deleted successfully!")
                    self.refresh_suppliers()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error deleting supplier: {e}")
    
    def view_supplier_products(self):
        """View products from selected supplier"""
        selected_item = self.suppliers_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a supplier to view their products.")
            return
        
        item_values = self.suppliers_tree.item(selected_item[0])['values']
        company_name = item_values[1]
        
        SupplierProductsDialog(self.root, company_name, self.db_config)
    
    def search_suppliers(self):
        """Search suppliers by company name or contact person"""
        search_term = self.search_entry.get().strip().lower()
        
        # Clear and reload filtered data
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                if search_term:
                    query = """
                        SELECT s.id, s.company_name, s.contact_person, s.phone, s.email, s.address,
                               COUNT(p.id) as product_count
                        FROM suppliers s
                        LEFT JOIN products p ON s.company_name = p.supplier
                        WHERE LOWER(s.company_name) LIKE %s OR LOWER(s.contact_person) LIKE %s
                        GROUP BY s.id, s.company_name, s.contact_person, s.phone, s.email, s.address
                        ORDER BY s.company_name
                    """
                    search_pattern = f"%{search_term}%"
                    cursor.execute(query, (search_pattern, search_pattern))
                else:
                    cursor.execute("""
                        SELECT s.id, s.company_name, s.contact_person, s.phone, s.email, s.address,
                               COUNT(p.id) as product_count
                        FROM suppliers s
                        LEFT JOIN products p ON s.company_name = p.supplier
                        GROUP BY s.id, s.company_name, s.contact_person, s.phone, s.email, s.address
                        ORDER BY s.company_name
                    """)
                
                suppliers = cursor.fetchall()
                
                for supplier in suppliers:
                    self.suppliers_tree.insert('', 'end', values=supplier)
                
                self.status_var.set(f"Found {len(suppliers)} suppliers")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error searching suppliers: {e}")
    
    def on_closing(self):
        """Handle window close"""
        self.root.destroy()


class SupplierDialog:
    def __init__(self, parent, title, data=None):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("450x400")
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
        tk.Label(main_frame, text="Company Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', pady=5)
        self.company_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.company_entry.grid(row=0, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Contact Person:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', pady=5)
        self.contact_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.contact_entry.grid(row=1, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Phone:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', pady=5)
        self.phone_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.phone_entry.grid(row=2, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Email:", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky='w', pady=5)
        self.email_entry = tk.Entry(main_frame, font=("Arial", 10), width=30)
        self.email_entry.grid(row=3, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Address:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky='nw', pady=5)
        self.address_text = tk.Text(main_frame, font=("Arial", 10), width=30, height=4)
        self.address_text.grid(row=4, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        tk.Label(main_frame, text="Notes:", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky='nw', pady=5)
        self.notes_text = tk.Text(main_frame, font=("Arial", 10), width=30, height=3)
        self.notes_text.grid(row=5, column=1, sticky='ew', pady=5, padx=(10, 0))
        
        # Configure grid
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Fill data if editing
        if data:
            self.company_entry.insert(0, data[0] or '')
            self.contact_entry.insert(0, data[1] or '')
            self.phone_entry.insert(0, data[2] or '')
            self.email_entry.insert(0, data[3] or '')
            if data[4]:
                self.address_text.insert(1.0, data[4])
            if data[5]:
                self.notes_text.insert(1.0, data[5])
        
        # Focus on first field
        self.company_entry.focus()
        
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
            command=self.save_supplier
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
        self.dialog.bind('<Return>', lambda e: self.save_supplier())
        self.dialog.bind('<Escape>', lambda e: self.cancel())
    
    def save_supplier(self):
        """Save supplier data"""
        # Get values
        company_name = self.company_entry.get().strip()
        contact_person = self.contact_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get(1.0, tk.END).strip()
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        # Validate
        if not company_name:
            messagebox.showerror("Validation Error", "Company name is required!")
            self.company_entry.focus()
            return
        
        # Store result
        self.result = (company_name, contact_person, phone, email, address, notes)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class SupplierProductsDialog:
    def __init__(self, parent, supplier_name, db_config):
        self.db_config = db_config
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Products from {supplier_name}")
        self.dialog.geometry("700x400")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Load and display products
        self.load_supplier_products(supplier_name)
    
    def load_supplier_products(self, supplier_name):
        """Load and display supplier products"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_label = tk.Label(main_frame, text=f"Products supplied by: {supplier_name}", 
                               font=("Arial", 14, "bold"))
        header_label.pack(pady=(0, 15))
        
        # Products table
        columns = ('ID', 'Product Name', 'Description', 'Price', 'Quantity', 'Category')
        products_tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        
        column_widths = [50, 150, 180, 100, 80, 120]
        for i, col in enumerate(columns):
            products_tree.heading(col, text=col)
            products_tree.column(col, width=column_widths[i])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(main_frame, orient='vertical', command=products_tree.yview)
        products_tree.configure(yscrollcommand=v_scrollbar.set)
        
        products_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Load products data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, name, description, price, quantity, category
                    FROM products 
                    WHERE supplier = %s
                    ORDER BY name
                """, (supplier_name,))
                products = cursor.fetchall()
                
                for product in products:
                    formatted_product = list(product)
                    formatted_product[3] = f"₹{product[3]:,.2f}"
                    products_tree.insert('', 'end', values=formatted_product)
                
                cursor.close()
                connection.close()
                
                # Summary
                summary_label = tk.Label(main_frame, text=f"Total Products: {len(products)}", 
                                       font=("Arial", 12))
                summary_label.pack(pady=10)
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading products: {e}")
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", command=self.dialog.destroy, 
                             font=("Arial", 11, "bold"), bg='#757575')
        close_btn.pack(pady=10)


if __name__ == "__main__":
    # For testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    app = SuppliersWindow(root)
    root.mainloop()