import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_config import DatabaseConfig

class ReportsWindow:
    def __init__(self, parent_window):
        self.parent = parent_window
        self.db_config = DatabaseConfig()
        
        # Create reports window
        self.root = tk.Toplevel()
        self.root.title("Warehouse Management - Reports")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Create interface
        self.create_widgets()
        
        # Load dashboard by default
        self.load_dashboard()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        """Create and arrange all widgets"""
        # Header Frame
        header_frame = tk.Frame(self.root, bg='#06FFA5', height=50)
        header_frame.pack(fill='x')
        header_frame.pack_propagate(False)
        
        header_label = tk.Label(
            header_frame,
            text="Reports & Analytics",
            font=("Arial", 16, "bold"),
            bg='#06FFA5',
            fg='black'
        )
        header_label.pack(pady=10)
        
        # Main Container
        main_container = tk.Frame(self.root)
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left Panel - Report Types
        left_panel = tk.Frame(main_container, width=200)
        left_panel.pack(side='left', fill='y', padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Report Type Selection
        reports_frame = tk.LabelFrame(left_panel, text="Report Types", font=("Arial", 12, "bold"))
        reports_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        # Report buttons
        report_buttons = [
            ("Dashboard", self.load_dashboard, "#4CAF50"),
            ("Inventory Report", self.inventory_report, "#2196F3"),
            ("Sales Report", self.sales_report, "#FF9800"),
            ("Low Stock Alert", self.low_stock_report, "#F44336"),
            ("Supplier Report", self.supplier_report, "#9C27B0"),
            ("Monthly Summary", self.monthly_summary, "#607D8B"),
        ]
        
        for text, command, color in report_buttons:
            btn = tk.Button(
                reports_frame,
                text=text,
                font=("Arial", 10, "bold"),
                bg=color,
                fg='black' if color in ['#2196F3', '#F44336', '#9C27B0', '#607D8B'] else 'black',
                command=command,
                cursor='hand2',
                width=20,
                pady=8
            )
            btn.pack(pady=5, padx=10, fill='x')
        
        # Date Filter Frame
        date_frame = tk.LabelFrame(left_panel, text="Date Filter", font=("Arial", 12, "bold"))
        date_frame.pack(fill='x', padx=5, pady=5)
        
        tk.Label(date_frame, text="From Date:", font=("Arial", 9)).pack(anchor='w', padx=5)
        self.from_date_entry = tk.Entry(date_frame, width=15)
        self.from_date_entry.pack(padx=5, pady=2)
        self.from_date_entry.insert(0, (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"))
        
        tk.Label(date_frame, text="To Date:", font=("Arial", 9)).pack(anchor='w', padx=5)
        self.to_date_entry = tk.Entry(date_frame, width=15)
        self.to_date_entry.pack(padx=5, pady=2)
        self.to_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        apply_filter_btn = tk.Button(
            date_frame,
            text="Apply Filter",
            font=("Arial", 9, "bold"),
            bg='#FF5722',
            fg='black',
            command=self.apply_date_filter,
            cursor='hand2'
        )
        apply_filter_btn.pack(pady=5, padx=5)
        
        # Right Panel - Content Area
        self.content_frame = tk.Frame(main_container)
        self.content_frame.pack(side='right', fill='both', expand=True)
        
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
        self.status_var.set("Ready - Select a report type from the left panel")
    
    def clear_content(self):
        """Clear the content frame"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def load_dashboard(self):
        """Load dashboard with key metrics"""
        self.clear_content()
        
        # Dashboard title
        title_label = tk.Label(
            self.content_frame,
            text="Warehouse Dashboard",
            font=("Arial", 18, "bold")
        )
        title_label.pack(pady=10)
        
        # Create metrics frame
        metrics_frame = tk.Frame(self.content_frame)
        metrics_frame.pack(fill='x', pady=10)
        
        # Get dashboard data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Total Products
                cursor.execute("SELECT COUNT(*) FROM products")
                total_products = cursor.fetchone()[0]
                
                # Total Orders
                cursor.execute("SELECT COUNT(*) FROM orders")
                total_orders = cursor.fetchone()[0]
                
                # Total Suppliers
                cursor.execute("SELECT COUNT(*) FROM suppliers")
                total_suppliers = cursor.fetchone()[0]
                
                # Low Stock Count
                cursor.execute("SELECT COUNT(*) FROM products WHERE quantity < 10")
                low_stock_count = cursor.fetchone()[0]
                
                # Total Sales
                cursor.execute("SELECT SUM(total_amount) FROM orders WHERE status != 'Cancelled'")
                total_sales = cursor.fetchone()[0] or 0
                
                # Recent Orders
                cursor.execute("""
                    SELECT COUNT(*) FROM orders 
                    WHERE order_date >= DATE_SUB(NOW(), INTERVAL 7 DAY)
                """)
                recent_orders = cursor.fetchone()[0]
                
                cursor.close()
                connection.close()
                
                # Create metric cards
                metrics = [
                    ("Total Products", total_products, "#4CAF50"),
                    ("Total Orders", total_orders, "#2196F3"),
                    ("Total Suppliers", total_suppliers, "#FF9800"),
                    ("Low Stock Items", low_stock_count, "#F44336"),
                    ("Total Sales", f"₹{total_sales:,.2f}", "#9C27B0"),
                    ("Orders (7 days)", recent_orders, "#607D8B")
                ]
                
                # Create cards in grid
                for i, (title, value, color) in enumerate(metrics):
                    row = i // 3
                    col = i % 3
                    
                    card_frame = tk.Frame(metrics_frame, bg=color, relief='raised', bd=2)
                    card_frame.grid(row=row, column=col, padx=10, pady=10, sticky='nsew')
                    
                    tk.Label(
                        card_frame,
                        text=str(value),
                        font=("Arial", 20, "bold"),
                        bg=color,
                        fg='white'
                    ).pack(pady=(10, 5))
                    
                    tk.Label(
                        card_frame,
                        text=title,
                        font=("Arial", 12),
                        bg=color,
                        fg='white'
                    ).pack(pady=(0, 10))
                
                # Configure grid weights
                for i in range(3):
                    metrics_frame.grid_columnconfigure(i, weight=1)
                
                self.status_var.set("Dashboard loaded successfully")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading dashboard: {e}")
                self.status_var.set("Error loading dashboard")
    
    def inventory_report(self):
        """Generate inventory report"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Inventory Report",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create table frame
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Create Treeview
        columns = ('Product ID', 'Product Name', 'Category', 'Quantity', 'Price', 'Total Value', 'Supplier')
        inventory_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        column_widths = [80, 150, 100, 80, 100, 120, 120]
        for i, col in enumerate(columns):
            inventory_tree.heading(col, text=col)
            inventory_tree.column(col, width=column_widths[i])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=inventory_tree.yview)
        inventory_tree.configure(yscrollcommand=v_scrollbar.set)
        
        inventory_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Load data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT id, name, category, quantity, price, (quantity * price) as total_value, supplier
                    FROM products
                    ORDER BY total_value DESC
                """)
                products = cursor.fetchall()
                
                total_inventory_value = 0
                for product in products:
                    formatted_product = list(product)
                    formatted_product[4] = f"₹{product[4]:,.2f}"  # Price
                    formatted_product[5] = f"₹{product[5]:,.2f}"  # Total Value
                    total_inventory_value += product[5]
                    inventory_tree.insert('', 'end', values=formatted_product)
                
                cursor.close()
                connection.close()
                
                # Summary
                summary_label = tk.Label(
                    self.content_frame,
                    text=f"Total Inventory Value: ₹{total_inventory_value:,.2f} | Total Products: {len(products)}",
                    font=("Arial", 14, "bold")
                )
                summary_label.pack(pady=10)
                
                self.status_var.set(f"Inventory report loaded - {len(products)} products")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading inventory report: {e}")
    
    def sales_report(self):
        """Generate sales report"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Sales Report",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create table frame
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Create Treeview
        columns = ('Order ID', 'Customer', 'Order Date', 'Status', 'Total Amount', 'Items Count')
        sales_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        column_widths = [80, 150, 120, 100, 120, 100]
        for i, col in enumerate(columns):
            sales_tree.heading(col, text=col)
            sales_tree.column(col, width=column_widths[i])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=sales_tree.yview)
        sales_tree.configure(yscrollcommand=v_scrollbar.set)
        
        sales_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Load data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT o.id, o.customer_name, o.order_date, o.status, o.total_amount,
                           COUNT(oi.id) as items_count
                    FROM orders o
                    LEFT JOIN order_items oi ON o.id = oi.order_id
                    WHERE o.order_date BETWEEN %s AND %s
                    GROUP BY o.id, o.customer_name, o.order_date, o.status, o.total_amount
                    ORDER BY o.order_date DESC
                """, (self.from_date_entry.get(), self.to_date_entry.get()))
                
                orders = cursor.fetchall()
                
                total_sales = 0
                completed_orders = 0
                
                for order in orders:
                    formatted_order = list(order)
                    formatted_order[2] = order[2].strftime("%Y-%m-%d")  # Date
                    formatted_order[4] = f"₹{order[4]:,.2f}"  # Amount
                    sales_tree.insert('', 'end', values=formatted_order)
                    
                    if order[3] != 'Cancelled':
                        total_sales += order[4]
                        if order[3] == 'Delivered':
                            completed_orders += 1
                
                cursor.close()
                connection.close()
                
                # Summary
                summary_frame = tk.Frame(self.content_frame)
                summary_frame.pack(pady=10)
                
                tk.Label(
                    summary_frame,
                    text=f"Total Sales: ₹{total_sales:,.2f}",
                    font=("Arial", 14, "bold")
                ).pack(side='left', padx=20)
                
                tk.Label(
                    summary_frame,
                    text=f"Total Orders: {len(orders)}",
                    font=("Arial", 14, "bold")
                ).pack(side='left', padx=20)
                
                tk.Label(
                    summary_frame,
                    text=f"Completed Orders: {completed_orders}",
                    font=("Arial", 14, "bold")
                ).pack(side='left', padx=20)
                
                self.status_var.set(f"Sales report loaded - {len(orders)} orders")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading sales report: {e}")
    
    def low_stock_report(self):
        """Generate low stock alert report"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Low Stock Alert Report",
            font=("Arial", 16, "bold"),
            fg='red'
        )
        title_label.pack(pady=10)
        
        # Stock threshold frame
        threshold_frame = tk.Frame(self.content_frame)
        threshold_frame.pack(pady=5)
        
        tk.Label(threshold_frame, text="Stock Threshold:", font=("Arial", 11)).pack(side='left')
        self.threshold_entry = tk.Entry(threshold_frame, width=10)
        self.threshold_entry.pack(side='left', padx=5)
        self.threshold_entry.insert(0, "10")
        
        tk.Button(
            threshold_frame,
            text="Update",
            command=self.low_stock_report,
            bg='#FF9800'
        ).pack(side='left', padx=5)
        
        # Create table frame
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Create Treeview
        columns = ('Product ID', 'Product Name', 'Current Stock', 'Category', 'Price', 'Supplier')
        stock_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        column_widths = [80, 180, 100, 120, 100, 150]
        for i, col in enumerate(columns):
            stock_tree.heading(col, text=col)
            stock_tree.column(col, width=column_widths[i])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=stock_tree.yview)
        stock_tree.configure(yscrollcommand=v_scrollbar.set)
        
        stock_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Load data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                threshold = int(self.threshold_entry.get() or 10)
                
                cursor.execute("""
                    SELECT id, name, quantity, category, price, supplier
                    FROM products
                    WHERE quantity <= %s
                    ORDER BY quantity ASC
                """, (threshold,))
                
                products = cursor.fetchall()
                
                for product in products:
                    formatted_product = list(product)
                    formatted_product[4] = f"₹{product[4]:,.2f}"  # Price
                    
                    # Color code based on stock level
                    if product[2] == 0:
                        stock_tree.insert('', 'end', values=formatted_product, tags=('out_of_stock',))
                    elif product[2] <= 5:
                        stock_tree.insert('', 'end', values=formatted_product, tags=('critical',))
                    else:
                        stock_tree.insert('', 'end', values=formatted_product, tags=('low',))
                
                # Configure tags
                stock_tree.tag_configure('out_of_stock', background='#ffcccc')
                stock_tree.tag_configure('critical', background='#ffe6cc')
                stock_tree.tag_configure('low', background='#fff2cc')
                
                cursor.close()
                connection.close()
                
                # Summary
                summary_label = tk.Label(
                    self.content_frame,
                    text=f"Products with stock ≤ {threshold}: {len(products)}",
                    font=("Arial", 14, "bold"),
                    fg='red' if products else 'green'
                )
                summary_label.pack(pady=10)
                
                if not products:
                    tk.Label(
                        self.content_frame,
                        text="🎉 All products have adequate stock!",
                        font=("Arial", 16),
                        fg='green'
                    ).pack(pady=20)
                
                self.status_var.set(f"Low stock report loaded - {len(products)} items need attention")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading low stock report: {e}")
    
    def supplier_report(self):
        """Generate supplier report"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Supplier Report",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Create table frame
        table_frame = tk.Frame(self.content_frame)
        table_frame.pack(fill='both', expand=True, pady=10)
        
        # Create Treeview
        columns = ('Supplier ID', 'Company Name', 'Contact Person', 'Phone', 'Email', 'Products Count', 'Total Inventory Value')
        supplier_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        column_widths = [80, 150, 120, 120, 150, 100, 150]
        for i, col in enumerate(columns):
            supplier_tree.heading(col, text=col)
            supplier_tree.column(col, width=column_widths[i])
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=supplier_tree.yview)
        supplier_tree.configure(yscrollcommand=v_scrollbar.set)
        
        supplier_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        
        # Load data
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute("""
                    SELECT s.id, s.company_name, s.contact_person, s.phone, s.email,
                           COUNT(p.id) as product_count,
                           COALESCE(SUM(p.quantity * p.price), 0) as total_value
                    FROM suppliers s
                    LEFT JOIN products p ON s.company_name = p.supplier
                    GROUP BY s.id, s.company_name, s.contact_person, s.phone, s.email
                    ORDER BY total_value DESC
                """)
                
                suppliers = cursor.fetchall()
                
                total_value = 0
                for supplier in suppliers:
                    formatted_supplier = list(supplier)
                    formatted_supplier[6] = f"₹{supplier[6]:,.2f}"  # Total Value
                    total_value += supplier[6]
                    supplier_tree.insert('', 'end', values=formatted_supplier)
                
                cursor.close()
                connection.close()
                
                # Summary
                summary_label = tk.Label(
                    self.content_frame,
                    text=f"Total Suppliers: {len(suppliers)} | Combined Inventory Value: ₹{total_value:,.2f}",
                    font=("Arial", 14, "bold")
                )
                summary_label.pack(pady=10)
                
                self.status_var.set(f"Supplier report loaded - {len(suppliers)} suppliers")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading supplier report: {e}")
    
    def monthly_summary(self):
        """Generate monthly summary report"""
        self.clear_content()
        
        # Title
        title_label = tk.Label(
            self.content_frame,
            text="Monthly Summary Report",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Summary cards frame
        cards_frame = tk.Frame(self.content_frame)
        cards_frame.pack(fill='x', pady=10)
        
        connection = self.db_config.get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                
                # Current month data
                current_month = datetime.now().strftime("%Y-%m")
                
                # Monthly orders
                cursor.execute("""
                    SELECT COUNT(*), SUM(total_amount)
                    FROM orders 
                    WHERE DATE_FORMAT(order_date, '%%Y-%%m') = %s
                """, (current_month,))
                month_orders, month_sales = cursor.fetchone()
                month_sales = month_sales or 0
                
                # Previous month comparison
                prev_month = (datetime.now().replace(day=1) - timedelta(days=1)).strftime("%Y-%m")
                cursor.execute("""
                    SELECT COUNT(*), SUM(total_amount)
                    FROM orders 
                    WHERE DATE_FORMAT(order_date, '%%Y-%%m') = %s
                """, (prev_month,))
                prev_orders, prev_sales = cursor.fetchone()
                prev_sales = prev_sales or 0
                
                # Calculate growth
                order_growth = ((month_orders - (prev_orders or 0)) / max(prev_orders or 1, 1)) * 100
                sales_growth = ((month_sales - prev_sales) / max(prev_sales, 1)) * 100
                
                # Top selling products this month
                cursor.execute("""
                    SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.total_price) as total_revenue
                    FROM order_items oi
                    JOIN products p ON oi.product_id = p.id
                    JOIN orders o ON oi.order_id = o.id
                    WHERE DATE_FORMAT(o.order_date, '%%Y-%%m') = %s
                    GROUP BY p.id, p.name
                    ORDER BY total_sold DESC
                    LIMIT 5
                """, (current_month,))
                top_products = cursor.fetchall()
                
                cursor.close()
                connection.close()
                
                # Create summary cards
                summaries = [
                    ("This Month Orders", f"{month_orders}", f"{order_growth:+.1f}%", "#2196F3"),
                    ("This Month Sales", f"₹{month_sales:,.2f}", f"{sales_growth:+.1f}%", "#4CAF50"),
                    ("Previous Month Orders", f"{prev_orders or 0}", "", "#FF9800"),
                    ("Previous Month Sales", f"₹{prev_sales:,.2f}", "", "#9C27B0")
                ]
                
                for i, (title, value, growth, color) in enumerate(summaries):
                    card_frame = tk.Frame(cards_frame, bg=color, relief='raised', bd=2)
                    card_frame.grid(row=i//2, column=i%2, padx=10, pady=10, sticky='nsew')
                    
                    tk.Label(card_frame, text=value, font=("Arial", 18, "bold"), 
                            bg=color, fg='white').pack(pady=(10, 5))
                    tk.Label(card_frame, text=title, font=("Arial", 11), 
                            bg=color, fg='white').pack()
                    if growth:
                        growth_color = 'lightgreen' if growth.startswith('+') else 'lightcoral'
                        tk.Label(card_frame, text=growth, font=("Arial", 10, "bold"), 
                                bg=color, fg=growth_color).pack(pady=(0, 10))
                    else:
                        tk.Label(card_frame, text=" ", font=("Arial", 10)).pack(pady=(0, 10))
                
                # Configure grid
                cards_frame.grid_columnconfigure(0, weight=1)
                cards_frame.grid_columnconfigure(1, weight=1)
                
                # Top Products Section
                if top_products:
                    top_products_frame = tk.LabelFrame(
                        self.content_frame, 
                        text=f"Top Selling Products - {current_month}", 
                        font=("Arial", 14, "bold")
                    )
                    top_products_frame.pack(fill='x', pady=20, padx=20)
                    
                    for i, (product_name, quantity, revenue) in enumerate(top_products, 1):
                        product_info = tk.Label(
                            top_products_frame,
                            text=f"{i}. {product_name} - Sold: {quantity} units - Revenue: ₹{revenue:,.2f}",
                            font=("Arial", 11),
                            anchor='w'
                        )
                        product_info.pack(fill='x', padx=10, pady=2)
                
                self.status_var.set(f"Monthly summary loaded for {current_month}")
                
            except Exception as e:
                messagebox.showerror("Database Error", f"Error loading monthly summary: {e}")
    
    def apply_date_filter(self):
        """Apply date filter and reload current report"""
        try:
            # Validate dates
            datetime.strptime(self.from_date_entry.get(), "%Y-%m-%d")
            datetime.strptime(self.to_date_entry.get(), "%Y-%m-%d")
            
            # Reload current report (you can track which report is currently shown)
            messagebox.showinfo("Date Filter", "Date filter applied. Please reload the desired report.")
            
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter dates in YYYY-MM-DD format.")
    
    def on_closing(self):
        """Handle window close"""
        self.root.destroy()


if __name__ == "__main__":
    # For testing
    try:
        root = tk.Tk()
        root.withdraw()  # Hide main window
        app = ReportsWindow(root)
        root.mainloop()
    except ImportError:
        messagebox.showerror("Missing Module", "matplotlib is required for reports. Install with: pip install matplotlib")
        import sys
        sys.exit(1)