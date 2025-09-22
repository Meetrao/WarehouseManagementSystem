import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from db_config import DatabaseConfig

class OrdersWindow:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.db_config = DatabaseConfig()
        
        # Create orders window
        self.root = tk.Toplevel()
        self.root.title("Warehouse Management - Orders")
        self.root.geometry("1000x600")
        self.root.resizable(True, True)
        
        # Create interface
        self.create_widgets()
        
        # Load initial data
        self.refresh_orders()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#FF6B35', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Orders Management",
            font=("Arial", 16, "bold"),
            bg='#FF6B35',
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
            text="Create New Order",
            font=("Arial", 11, "bold"),
            bg='#4CAF50',
            fg='black',
            command=self.create_order,
            cursor='hand2'
        )
        btn_add.pack(side='left', padx=(0, 10))
        
        btn_view = tk.Button(
            buttons_frame,
            text="View Order Details",
            font=("Arial", 11, "bold"),
            bg='#2196F3',
            fg='black',
            command=self.view_order_details,
            cursor='hand2'
        )
        btn_view.pack(side='left', padx=(0, 10))
        
        btn_update_status = tk.Button(
            buttons_frame,
            text="Update Status",
            font=("Arial", 11, "bold"),
            bg='#FF9800',
            fg='black',
            command=self.update_order_status,
            cursor='hand2'
        )
        btn_update_status.pack(side='left', padx=(0, 10))
        
        btn_delete = tk.Button(
            buttons_frame,
            text="Delete Order",
            font=("Arial", 11, "bold"),
            bg='#F44336',
            fg='black',
            command=self.delete_order,
            cursor='hand2'
        )
        btn_delete.pack(side='left', padx=(0, 10))
        
        btn_refresh = tk.Button(
            buttons_frame,
            text="Refresh",
            font=("Arial", 11, "bold"),
            bg='#607D8B',
            fg='black',
            command=self.refresh_orders,
            cursor='hand2'
        )
        btn_refresh.pack(side='left', padx=(0, 10))
        
        # Filter Frame
        filter_frame = tk.Frame(buttons_frame)
        filter_frame.pack(side='right')
        
        tk.Label(filter_frame, text="Status Filter:", font=("Arial", 10)).pack(side='left')
        self.status_filter = ttk.Combobox(
            filter_frame, 
            values=["All", "Pending", "Processing", "Shipped", "Delivered", "Cancelled"],
            state="readonly",
            width=12
        )
        self.status_filter.set("All")
        self.status_filter.pack(side='left', padx=(5, 5))
        self.status_filter.bind("<<ComboboxSelected>>", lambda e: self.filter_orders())
        
        # Orders Table Frame
        table_frame = tk.Frame(main_container)
        table_frame.pack(fill='both', expand=True)
        
        # Create Treeview (Table)
        columns = ('ID', 'Customer', 'Total Amount', 'Status', 'Order Date', 'Items Count')
        self.orders_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # Define column headings and widths
        column_widths = [80, 200, 120, 100, 150, 100]
        for i, col in enumerate(columns):
            self.orders_tree.heading(col, text=col)
            self.orders_tree.column(col, width=column_widths[i], minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.orders_tree.yview)
        self.orders_tree.configure(yscrollcommand=v_scrollbar.set)
        
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.orders_tree.xview)
        self.orders_tree.configure(xscrollcommand=h_scrollbar.set)
        
        # Pack table and scrollbars
        self.orders_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Bind double-click to view details
        self.orders_tree.bind('<Double-1>', lambda e: self.view_order_details())
        
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
    
    def refresh_orders(self):
        """Refresh the orders table"""
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT o.id, o.customer_name, o.total_amount, o.status, o.order_date,
                           COUNT(oi.id) as item_count
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    GROUP BY o.id, o.customer_name, o.total_amount, o.status, o.order_date
                    ORDER BY o.order_date DESC
                """)
                orders = cursor.fetchall()
                
                # Insert orders into table
                for order in orders:
                    formatted_order = list(order)
                    formatted_order[2] = f"₹{order[2]:,.2f}"  # Format amount
                    formatted_order[4] = order[4].strftime("%Y-%m-%d %H:%M")  # Format date
                    self.orders_tree.insert('', 'end', values=formatted_order)
                
                self.status_var.set(f"Loaded {len(orders)} orders")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading orders: {e}")
                self.status_var.set("Error loading orders")
    
    def create_order(self):
        """Create a new order"""
        dialog = CreateOrderDialog(self.root)
        if dialog.result:
            order_data, order_items = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    
                    # Insert order
                    order_query = """
                        INSERT INTO orders (customer_name, customer_phone, customer_address, 
                                          total_amount, status, order_date)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(order_query, order_data)
                    order_id = cursor.lastrowid
                    
                    # Insert order items
                    item_query = """
                        INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price)
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    for item in order_items:
                        cursor.execute(item_query, (order_id,) + item)
                    
                    # Update product quantities
                    for item in order_items:
                        product_id, quantity = item[0], item[1]
                        cursor.execute("""
                            UPDATE products SET quantity = quantity - %s WHERE id = %s
                        """, (quantity, product_id))
                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", f"Order #{order_id} created successfully!")
                    self.refresh_orders()
                    
                except Exception as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error creating order: {e}")
    
    def view_order_details(self):
        """View detailed information about selected order"""
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an order to view details.")
            return
        
        item_values = self.orders_tree.item(selected_item[0])['values']
        order_id = item_values[0]
        
        OrderDetailsDialog(self.root, order_id, self.db_config)
    
    def update_order_status(self):
        """Update status of selected order"""
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an order to update status.")
            return
        
        item_values = self.orders_tree.item(selected_item[0])['values']
        order_id = item_values[0]
        current_status = item_values[3]
        
        dialog = UpdateStatusDialog(self.root, current_status)
        if dialog.result:
            new_status = dialog.result
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    cursor.execute("""
                        UPDATE orders SET status = %s WHERE id = %s
                    """, (new_status, order_id))
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", f"Order status updated to '{new_status}'!")
                    self.refresh_orders()
                    
                except Exception as e:
                    messagebox.showerror("Database Error", f"Error updating order status: {e}")
    
    def delete_order(self):
        """Delete selected order"""
        selected_item = self.orders_tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an order to delete.")
            return
        
        item_values = self.orders_tree.item(selected_item[0])['values']
        order_id = item_values[0]
        customer_name = item_values[1]
        
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete order #{order_id} for {customer_name}?"):
            connection = self.db_config.get_connection()
            if connection:
                try:
                    cursor = connection.cursor()
                    
                    # Get order items to restore product quantities
                    cursor.execute("""
                        SELECT product_id, quantity FROM order_items WHERE order_id = %s
                    """, (order_id,))
                    order_items = cursor.fetchall()
                    
                    # Restore product quantities
                    for product_id, quantity in order_items:
                        cursor.execute("""
                            UPDATE products SET quantity = quantity + %s WHERE id = %s
                        """, (quantity, product_id))
                    
                    # Delete order items first (foreign key constraint)
                    cursor.execute("DELETE FROM order_items WHERE order_id = %s", (order_id,))
                    
                    # Delete order
                    cursor.execute("DELETE FROM orders WHERE id = %s", (order_id,))
                    
                    connection.commit()
                    cursor.close()
                    connection.close()
                    
                    messagebox.showinfo("Success", "Order deleted successfully!")
                    self.refresh_orders()
                    
                except Exception as e:
                    connection.rollback()
                    messagebox.showerror("Database Error", f"Error deleting order: {e}")
    
    def filter_orders(self):
        """Filter orders by status"""
        status_filter = self.status_filter.get()
        
        # Clear existing items
        for item in self.orders_tree.get_children():
            self.orders_tree.delete(item)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                if status_filter == "All":
                    cursor.execute("""
                        SELECT o.id, o.customer_name, o.total_amount, o.status, o.order_date,
                               COUNT(oi.id) as item_count
                        FROM orders o
                        LEFT JOIN order_items oi ON o.id = oi.order_id
                        GROUP BY o.id, o.customer_name, o.total_amount, o.status, o.order_date
                        ORDER BY o.order_date DESC
                    """)
                else:
                    cursor.execute("""
                        SELECT o.id, o.customer_name, o.total_amount, o.status, o.order_date,
                               COUNT(oi.id) as item_count
                        FROM orders o
                        LEFT JOIN order_items oi ON o.id = oi.order_id
                        WHERE o.status = %s
                        GROUP BY o.id, o.customer_name, o.total_amount, o.status, o.order_date
                        ORDER BY o.order_date DESC
                    """, (status_filter,))
                
                orders = cursor.fetchall()
                
                for order in orders:
                    formatted_order = list(order)
                    formatted_order[2] = f"₹{order[2]:,.2f}"
                    formatted_order[4] = order[4].strftime("%Y-%m-%d %H:%M")
                    self.orders_tree.insert('', 'end', values=formatted_order)
                
                self.status_var.set(f"Filtered {len(orders)} orders")
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error filtering orders: {e}")
    
    def on_closing(self):
        """Handle window close"""
        self.root.destroy()


class CreateOrderDialog:
    def __init__(self, parent):
        self.result = None
        self.db_config = DatabaseConfig()
        self.order_items = []
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create New Order")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form()
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self):
        """Create order form"""
        # Main frame with scrollbar
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Customer Information Section
        customer_frame = tk.LabelFrame(main_frame, text="Customer Information", font=("Arial", 12, "bold"))
        customer_frame.pack(fill='x', pady=(0, 15))
        
        # Customer fields
        tk.Label(customer_frame, text="Customer Name:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.customer_name_entry = tk.Entry(customer_frame, font=("Arial", 10), width=30)
        self.customer_name_entry.grid(row=0, column=1, sticky='ew', padx=10, pady=5)
        
        tk.Label(customer_frame, text="Phone:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.customer_phone_entry = tk.Entry(customer_frame, font=("Arial", 10), width=30)
        self.customer_phone_entry.grid(row=1, column=1, sticky='ew', padx=10, pady=5)
        
        tk.Label(customer_frame, text="Address:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.customer_address_text = tk.Text(customer_frame, font=("Arial", 10), height=3, width=30)
        self.customer_address_text.grid(row=2, column=1, sticky='ew', padx=10, pady=5)
        
        customer_frame.grid_columnconfigure(1, weight=1)
        
        # Order Items Section
        items_frame = tk.LabelFrame(main_frame, text="Order Items", font=("Arial", 12, "bold"))
        items_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        # Add item controls
        add_item_frame = tk.Frame(items_frame)
        add_item_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(add_item_frame, text="Product:").grid(row=0, column=0, padx=5)
        self.product_combo = ttk.Combobox(add_item_frame, width=20, state="readonly")
        self.product_combo.grid(row=0, column=1, padx=5)
        self.load_products()
        
        tk.Label(add_item_frame, text="Quantity:").grid(row=0, column=2, padx=5)
        self.quantity_entry = tk.Entry(add_item_frame, width=10)
        self.quantity_entry.grid(row=0, column=3, padx=5)
        
        add_btn = tk.Button(add_item_frame, text="Add Item", command=self.add_item, bg='#4CAF50')
        add_btn.grid(row=0, column=4, padx=10)
        
        # Items list
        items_list_frame = tk.Frame(items_frame)
        items_list_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        columns = ('Product', 'Quantity', 'Unit Price', 'Total')
        self.items_tree = ttk.Treeview(items_list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(items_list_frame, orient='vertical', command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.items_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Remove item button
        remove_btn = tk.Button(items_frame, text="Remove Selected Item", command=self.remove_item, bg='#F44336')
        remove_btn.pack(pady=5)
        
        # Total amount
        self.total_var = tk.StringVar()
        self.total_var.set("Total: ₹0.00")
        total_label = tk.Label(main_frame, textvariable=self.total_var, font=("Arial", 14, "bold"))
        total_label.pack(pady=10)
        
        # Buttons
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack(pady=10)
        
        save_btn = tk.Button(buttons_frame, text="Create Order", font=("Arial", 11, "bold"), 
                           bg='#4CAF50', command=self.save_order)
        save_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel", font=("Arial", 11, "bold"), 
                             bg='#757575', command=self.cancel)
        cancel_btn.pack(side='left', padx=10)
    
    def load_products(self):
        """Load products into combo box"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("SELECT id, name, price FROM products WHERE quantity > 0")
                products = cursor.fetchall()
                
                product_list = []
                self.product_data = {}
                for product in products:
                    display_text = f"{product[1]} - ₹{product[2]:,.2f}"
                    product_list.append(display_text)
                    self.product_data[display_text] = product
                
                self.product_combo['values'] = product_list
                cursor.close()
                connection.close()
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading products: {e}")
    
    def add_item(self):
        """Add item to order"""
        selected_product = self.product_combo.get()
        quantity_str = self.quantity_entry.get().strip()
        
        if not selected_product:
            messagebox.showwarning("Validation Error", "Please select a product!")
            return
        
        try:
            quantity = int(quantity_str)
            if quantity <= 0:
                raise ValueError()
        except ValueError:
            messagebox.showerror("Validation Error", "Please enter a valid quantity!")
            return
        
        # Get product data
        product_id, product_name, unit_price = self.product_data[selected_product]
        total_price = unit_price * quantity
        
        # Add to items list
        self.items_tree.insert('', 'end', values=(
            product_name, quantity, f"₹{unit_price:,.2f}", f"₹{total_price:,.2f}"
        ))
        
        # Store item data
        self.order_items.append((product_id, quantity, unit_price, total_price))
        
        # Update total
        self.update_total()
        
        # Clear inputs
        self.product_combo.set('')
        self.quantity_entry.delete(0, tk.END)
    
    def remove_item(self):
        """Remove selected item from order"""
        selected = self.items_tree.selection()
        if selected:
            index = self.items_tree.index(selected[0])
            self.items_tree.delete(selected[0])
            self.order_items.pop(index)
            self.update_total()
    
    def update_total(self):
        """Update total amount"""
        total = sum(item[3] for item in self.order_items)
        self.total_var.set(f"Total: ₹{total:,.2f}")
    
    def save_order(self):
        """Save the order"""
        # Validate customer info
        customer_name = self.customer_name_entry.get().strip()
        customer_phone = self.customer_phone_entry.get().strip()
        customer_address = self.customer_address_text.get(1.0, tk.END).strip()
        
        if not customer_name:
            messagebox.showerror("Validation Error", "Customer name is required!")
            return
        
        if not self.order_items:
            messagebox.showerror("Validation Error", "Please add at least one item to the order!")
            return
        
        # Calculate total
        total_amount = sum(item[3] for item in self.order_items)
        
        # Prepare order data
        order_data = (
            customer_name,
            customer_phone,
            customer_address,
            total_amount,
            'Pending',
            datetime.now()
        )
        
        self.result = (order_data, self.order_items)
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


class OrderDetailsDialog:
    def __init__(self, parent, order_id, db_config):
        self.db_config = db_config
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Order Details - Order #{order_id}")
        self.dialog.geometry("600x500")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Load and display order details
        self.load_order_details(order_id)
    
    def load_order_details(self, order_id):
        """Load and display order details"""
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Get order info
                cursor.execute("""
                    SELECT customer_name, customer_phone, customer_address, 
                           total_amount, status, order_date
                    FROM orders WHERE id = %s
                """, (order_id,))
                order = cursor.fetchone()
                
                # Get order items
                cursor.execute("""
                    SELECT p.name, oi.quantity, oi.unit_price, oi.total_price
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    WHERE oi.order_id = %s
                """, (order_id,))
                items = cursor.fetchall()
                
                cursor.close()
                connection.close()
                
                if order:
                    self.display_order_details(order_id, order, items)
                else:
                    messagebox.showerror("Error", "Order not found!")
                    self.dialog.destroy()
                    
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading order details: {e}")
                self.dialog.destroy()
    
    def display_order_details(self, order_id, order, items):
        """Display order details in the dialog"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        # Order Header
        header_frame = tk.Frame(main_frame)
        header_frame.pack(fill='x', pady=(0, 20))
        
        tk.Label(header_frame, text=f"Order #{order_id}", font=("Arial", 18, "bold")).pack()
        tk.Label(header_frame, text=f"Status: {order[4]}", font=("Arial", 12)).pack()
        tk.Label(header_frame, text=f"Order Date: {order[5].strftime('%Y-%m-%d %H:%M')}", 
                font=("Arial", 10)).pack()
        
        # Customer Info
        customer_frame = tk.LabelFrame(main_frame, text="Customer Information", font=("Arial", 12, "bold"))
        customer_frame.pack(fill='x', pady=(0, 15))
        
        tk.Label(customer_frame, text=f"Name: {order[0]}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=2)
        tk.Label(customer_frame, text=f"Phone: {order[1]}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=2)
        tk.Label(customer_frame, text=f"Address: {order[2]}", font=("Arial", 10)).pack(anchor='w', padx=10, pady=2)
        
        # Order Items
        items_frame = tk.LabelFrame(main_frame, text="Order Items", font=("Arial", 12, "bold"))
        items_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        columns = ('Product', 'Quantity', 'Unit Price', 'Total')
        items_tree = ttk.Treeview(items_frame, columns=columns, show='headings', height=10)
        
        for col in columns:
            items_tree.heading(col, text=col)
            items_tree.column(col, width=120)
        
        for item in items:
            items_tree.insert('', 'end', values=(
                item[0], item[1], f"₹{item[2]:,.2f}", f"₹{item[3]:,.2f}"
            ))
        
        items_tree.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Total
        total_label = tk.Label(main_frame, text=f"Total Amount: ₹{order[3]:,.2f}", 
                              font=("Arial", 14, "bold"))
        total_label.pack(pady=10)
        
        # Close button
        close_btn = tk.Button(main_frame, text="Close", command=self.dialog.destroy, 
                             font=("Arial", 11, "bold"), bg='#757575')
        close_btn.pack(pady=10)


class UpdateStatusDialog:
    def __init__(self, parent, current_status):
        self.result = None
        
        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Update Order Status")
        self.dialog.geometry("300x200")
        self.dialog.resizable(False, False)
        
        # Make dialog modal
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Create form
        self.create_form(current_status)
        
        # Wait for dialog to close
        self.dialog.wait_window()
    
    def create_form(self, current_status):
        """Create status update form"""
        main_frame = tk.Frame(self.dialog, padx=20, pady=20)
        main_frame.pack(fill='both', expand=True)
        
        tk.Label(main_frame, text=f"Current Status: {current_status}", 
                font=("Arial", 12, "bold")).pack(pady=(0, 20))
        
        tk.Label(main_frame, text="New Status:", font=("Arial", 10, "bold")).pack(anchor='w')
        
        self.status_combo = ttk.Combobox(
            main_frame, 
            values=["Pending", "Processing", "Shipped", "Delivered", "Cancelled"],
            state="readonly",
            width=20
        )
        self.status_combo.set(current_status)
        self.status_combo.pack(pady=(5, 20))
        
        # Buttons
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.pack()
        
        update_btn = tk.Button(buttons_frame, text="Update", font=("Arial", 11, "bold"), 
                              bg='#4CAF50', command=self.update_status)
        update_btn.pack(side='left', padx=10)
        
        cancel_btn = tk.Button(buttons_frame, text="Cancel", font=("Arial", 11, "bold"), 
                              bg='#757575', command=self.cancel)
        cancel_btn.pack(side='left', padx=10)
    
    def update_status(self):
        """Update the status"""
        self.result = self.status_combo.get()
        self.dialog.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.dialog.destroy()


if __name__ == "__main__":
    # For testing
    root = tk.Tk()
    root.withdraw()  # Hide main window
    app = OrdersWindow(root)
    root.mainloop()