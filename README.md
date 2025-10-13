# 🏭 Warehouse Management System

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![MySQL](https://img.shields.io/badge/MySQL-8.0%2B-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)

A comprehensive warehouse management system built with Python, Tkinter, and MySQL for managing inventory, orders, suppliers, and generating insightful reports.

[Features](#-features) •
[Installation](#-installation) •
[Usage](#-usage) •
[Documentation](#-documentation) •
[Screenshots](#-screenshots) •
[Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [System Requirements](#-system-requirements)
- [Installation](#-installation)
  - [Windows Setup](#windows-setup)
  - [macOS Setup](#macos-setup)
  - [Linux Setup](#linux-setup)
- [Database Setup](#-database-setup)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Usage Guide](#-usage-guide)
- [Project Structure](#-project-structure)
- [API Reference](#-api-reference)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [License](#-license)
- [Contact](#-contact)

---

## 🎯 Overview

The Warehouse Management System is a desktop application designed to streamline warehouse operations including inventory tracking, order management, supplier relationships, and business analytics. Built with a modern GUI using Tkinter and powered by MySQL database, this system provides a robust solution for small to medium-sized businesses.

### Key Highlights

- **User-Friendly Interface**: Intuitive GUI built with Tkinter
- **Real-Time Inventory**: Track stock levels with automatic updates
- **Order Management**: Create, track, and manage customer orders
- **Supplier Database**: Maintain comprehensive supplier information
- **Analytics Dashboard**: Generate reports and visualize data
- **Multi-User Support**: Role-based access control (Admin/User)
- **Data Backup**: Export/import functionality for data safety

---

## ✨ Features

### 📦 **Product Management**
- ✅ Add, edit, delete products
- ✅ Real-time inventory tracking
- ✅ Category-based organization
- ✅ Supplier linking
- ✅ Low stock alerts
- ✅ Bulk import/export (CSV)
- ✅ Advanced search and filtering

### 🛒 **Order Management**
- ✅ Create multi-item orders
- ✅ Customer information management
- ✅ Order status tracking (Pending → Processing → Shipped → Delivered)
- ✅ Automatic inventory deduction
- ✅ Order history and details view
- ✅ Status-based filtering
- ✅ Invoice generation ready

### 🏢 **Supplier Management**
- ✅ Comprehensive supplier database
- ✅ Contact information tracking
- ✅ Supplier-product relationship mapping
- ✅ Performance tracking
- ✅ Notes and communication history
- ✅ Supplier product catalog view

### 📊 **Reports & Analytics**
- ✅ Interactive dashboard with key metrics
- ✅ Inventory valuation reports
- ✅ Sales analytics
- ✅ Low stock alerts with threshold settings
- ✅ Supplier performance reports
- ✅ Monthly summary with growth trends
- ✅ Visual charts and graphs (matplotlib)
- ✅ Date-range filtering

### ⚙️ **System Settings**
- ✅ Company information configuration
- ✅ Currency settings
- ✅ Low stock threshold customization
- ✅ User management (Add/Edit/Delete users)
- ✅ Password management
- ✅ Database connection settings
- ✅ Backup and restore functionality
- ✅ Theme customization options

### 🔐 **Security Features**
- ✅ User authentication system
- ✅ Role-based access control
- ✅ Password-protected admin functions
- ✅ Session management
- ✅ Audit trail ready

---

## 💻 System Requirements

### Minimum Requirements

| Component | Requirement |
|-----------|------------|
| **Operating System** | Windows 10/11, macOS 10.14+, Ubuntu 18.04+ |
| **Python** | 3.8 or higher |
| **RAM** | 4 GB minimum (8 GB recommended) |
| **Storage** | 500 MB free space |
| **Display** | 1280x720 resolution minimum |
| **MySQL** | MySQL 8.0 or higher |

### Software Dependencies

```
Python 3.8+
MySQL Server 8.0+
pip (Python package manager)
```

### Python Libraries

```
mysql-connector-python >= 8.0.33
matplotlib >= 3.7.1
tkinter (included with Python)
```

---

## 🚀 Installation

### Windows Setup

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. ⚠️ **IMPORTANT**: Check ✅ **"Add Python to PATH"**
4. Click "Install Now"
5. Verify installation:

```bash
python --version
pip --version
```

#### Step 2: Install MySQL

1. Download MySQL from [MySQL Downloads](https://dev.mysql.com/downloads/installer/)
2. Choose "MySQL Installer for Windows"
3. Select "Developer Default" or "Server Only"
4. Set root password during installation (remember this!)
5. Complete the installation
6. Verify MySQL is running:

```bash
# Open Services (Win + R → services.msc)
# Find "MySQL80" and ensure it's "Running"
```

#### Step 3: Clone/Download Project

```bash
# Using Git
git clone https://github.com/yourusername/warehouse-management-system.git
cd warehouse-management-system

# Or download ZIP and extract
```

#### Step 4: Install Dependencies

```bash
# Install required Python packages
pip install mysql-connector-python matplotlib
```

#### Step 5: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv warehouse_env

# Activate virtual environment
warehouse_env\Scripts\activate

# Install dependencies in virtual environment
pip install mysql-connector-python matplotlib
```

---

### macOS Setup

#### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

#### Step 2: Install Python

```bash
brew install python
python3 --version
```

#### Step 3: Install MySQL

```bash
brew install mysql
brew services start mysql

# Secure MySQL installation
mysql_secure_installation
```

#### Step 4: Clone Project

```bash
git clone https://github.com/yourusername/warehouse-management-system.git
cd warehouse-management-system
```

#### Step 5: Setup Virtual Environment

```bash
python3 -m venv warehouse_env
source warehouse_env/bin/activate
pip install mysql-connector-python matplotlib
```

---

### Linux Setup

#### Step 1: Install Python & MySQL

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv mysql-server

# Fedora/RHEL
sudo dnf install python3 python3-pip mysql-server

# Start MySQL
sudo systemctl start mysql
sudo systemctl enable mysql
```

#### Step 2: Secure MySQL

```bash
sudo mysql_secure_installation
```

#### Step 3: Clone Project

```bash
git clone https://github.com/yourusername/warehouse-management-system.git
cd warehouse-management-system
```

#### Step 4: Setup Virtual Environment

```bash
python3 -m venv warehouse_env
source warehouse_env/bin/activate
pip install mysql-connector-python matplotlib
```

---

## 🗄️ Database Setup

### Method 1: Using SQL Script (Recommended)

1. **Create the SQL script file** `setup_database.sql` with the following content:

```sql
-- Create database
CREATE DATABASE IF NOT EXISTS warehouse_db;
USE warehouse_db;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Products table
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    quantity INT NOT NULL DEFAULT 0,
    category VARCHAR(100),
    supplier VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_person VARCHAR(255),
    phone VARCHAR(20),
    email VARCHAR(255),
    address TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(255) NOT NULL,
    customer_phone VARCHAR(20),
    customer_address TEXT,
    total_amount DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status ENUM('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled') DEFAULT 'Pending',
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Order items table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
);

-- Insert default admin user
INSERT INTO users (username, password, role) 
VALUES ('admin', 'admin123', 'admin');

-- Insert sample suppliers
INSERT INTO suppliers (company_name, contact_person, phone, email, address) VALUES 
('Tech Supplies Inc', 'John Smith', '+91-9876543210', 'john@techsupplies.com', '123 Tech Street, Mumbai, Maharashtra'),
('Global Electronics', 'Sarah Johnson', '+91-9876543211', 'sarah@globalelec.com', '456 Electronic Avenue, Delhi'),
('Office Solutions Ltd', 'Mike Wilson', '+91-9876543212', 'mike@officesol.com', '789 Business Park, Bangalore, Karnataka');

-- Insert sample products
INSERT INTO products (name, description, price, quantity, category, supplier) VALUES 
('Laptop Dell Inspiron 15', 'Dell Inspiron 15 with Intel Core i5, 8GB RAM, 512GB SSD', 45000.00, 25, 'Electronics', 'Tech Supplies Inc'),
('Wireless Mouse Logitech', 'Logitech M705 Marathon Wireless Mouse', 2500.00, 100, 'Electronics', 'Tech Supplies Inc'),
('Office Chair Executive', 'High-back executive office chair with lumbar support', 8500.00, 50, 'Furniture', 'Office Solutions Ltd'),
('HP LaserJet Printer', 'HP LaserJet Pro M404dn Printer', 18000.00, 15, 'Electronics', 'Global Electronics'),
('LED Desk Lamp', 'Adjustable LED desk lamp with USB charging port', 1200.00, 75, 'Furniture', 'Office Solutions Ltd'),
('External Hard Drive 1TB', 'Seagate Backup Plus Slim 1TB External HDD', 4500.00, 30, 'Electronics', 'Tech Supplies Inc'),
('Wooden Office Desk', '4ft x 2ft wooden office desk with drawers', 12000.00, 20, 'Furniture', 'Office Solutions Ltd'),
('HD Webcam 1080p', 'Logitech C920 HD Pro Webcam', 6500.00, 40, 'Electronics', 'Global Electronics'),
('Mechanical Keyboard', 'Corsair K95 RGB Platinum Mechanical Keyboard', 15000.00, 12, 'Electronics', 'Tech Supplies Inc'),
('5-Tier Bookshelf', 'Wooden 5-tier bookshelf', 3500.00, 25, 'Furniture', 'Office Solutions Ltd');
```

2. **Run the SQL script:**

```bash
# Windows (CMD)
mysql -u root -p < setup_database.sql

# macOS/Linux
mysql -u root -p < setup_database.sql

# Enter your MySQL root password when prompted
```

### Method 2: Manual Database Creation

```bash
# Connect to MySQL
mysql -u root -p

# Then run SQL commands manually
```

### Verify Database Setup

```bash
mysql -u root -p -e "USE warehouse_db; SHOW TABLES;"
mysql -u root -p -e "USE warehouse_db; SELECT COUNT(*) FROM products;"
```

You should see **5 tables** and **10 products**.

---

## ⚙️ Configuration

### Database Configuration

Edit `db_config.py`:

```python
class DatabaseConfig:
    def __init__(self):
        self.host = 'localhost'        # Database host
        self.database = 'warehouse_db' # Database name
        self.user = 'root'             # MySQL username
        self.password = 'your_password_here'  # ⚠️ Change this!
```

### Application Settings

Settings are stored in `warehouse_settings.json` (created automatically on first run):

```json
{
    "company_name": "Your Warehouse Company",
    "address": "",
    "phone": "",
    "email": "",
    "currency": "₹",
    "low_stock_threshold": 10,
    "auto_backup": true,
    "theme": "Default"
}
```

---

## 🎮 Running the Application

### Using Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd warehouse-management-system

# Activate virtual environment
# Windows:
warehouse_env\Scripts\activate

# macOS/Linux:
source warehouse_env/bin/activate

# Run the application
python main.py
```

### Direct Execution

```bash
# Navigate to project directory
cd warehouse-management-system

# Run directly
python main.py
```

### Default Login Credentials

```
Username: admin
Password: admin123
```

⚠️ **Change the default password after first login via Settings → Users**

---

## 📖 Usage Guide

### 1️⃣ Products Management

**Add New Product:**
1. Click "Manage Products" from dashboard
2. Click "Add New Product" button
3. Fill in product details:
   - Product Name (required)
   - Description
   - Price (required)
   - Quantity (required)
   - Category
   - Supplier
4. Click "Save"

**Edit Product:**
1. Select product from list
2. Click "Edit Product" or double-click the product
3. Modify details
4. Click "Save"

**Delete Product:**
1. Select product from list
2. Click "Delete Product"
3. Confirm deletion

**Search Products:**
1. Enter search term in search box
2. Click "Go" or press Enter
3. Search works on name, category, and supplier

---

### 2️⃣ Orders Management

**Create New Order:**
1. Click "Manage Orders" from dashboard
2. Click "Create New Order"
3. Enter customer information:
   - Customer Name (required)
   - Phone number
   - Address
4. Add items to order:
   - Select product from dropdown
   - Enter quantity
   - Click "Add Item"
5. Review order total
6. Click "Create Order"

**View Order Details:**
1. Select order from list
2. Click "View Order Details" or double-click
3. View complete order information

**Update Order Status:**
1. Select order from list
2. Click "Update Status"
3. Choose new status:
   - Pending
   - Processing
   - Shipped
   - Delivered
   - Cancelled
4. Click "Update"

**Filter Orders:**
- Use the status dropdown to filter orders by status
- Select "All" to view all orders

---

### 3️⃣ Suppliers Management

**Add New Supplier:**
1. Click "Manage Suppliers" from dashboard
2. Click "Add New Supplier"
3. Fill in supplier details:
   - Company Name (required)
   - Contact Person
   - Phone
   - Email
   - Address
   - Notes
4. Click "Save"

**View Supplier Products:**
1. Select supplier from list
2. Click "View Products"
3. See all products from this supplier

**Edit/Delete Supplier:**
- Similar to products management

---

### 4️⃣ Reports & Analytics

**Dashboard:**
- View key metrics at a glance
- Total products, orders, suppliers
- Low stock items count
- Total sales
- Recent orders (last 7 days)

**Inventory Report:**
- Complete product listing with values
- Total inventory valuation
- Stock levels

**Sales Report:**
- Order history within date range
- Total sales amount
- Order count by status
- Use date filter for custom ranges

**Low Stock Alert:**
- Products below threshold
- Color-coded by urgency:
  - Red: Out of stock
  - Orange: Critical (≤5 units)
  - Yellow: Low stock (≤10 units)
- Adjust threshold in Settings

**Supplier Report:**
- Supplier performance metrics
- Product count per supplier
- Total inventory value per supplier

**Monthly Summary:**
- Current month vs previous month comparison
- Growth percentages
- Top 5 selling products

---

### 5️⃣ System Settings

**General Settings:**
- Update company information
- Configure currency symbol
- Set low stock threshold
- Enable/disable auto backup
- Choose theme

**Database Settings:**
- View database connection info
- Test database connection
- View database statistics

**User Management:**
- Add new users
- Change user passwords
- Delete users
- Manage user roles (admin/user)

**Backup & Restore:**
- Create database backup
- Export products to CSV
- Import products from CSV

---

## 📁 Project Structure

```
warehouse-management-system/
│
├── main.py                      # Application entry point
├── login.py                     # Login window and authentication
├── dashboard.py                 # Main dashboard interface
├── db_config.py                 # Database configuration
│
├── products.py                  # Products management module
├── orders.py                    # Orders management module
├── suppliers.py                 # Suppliers management module
├── reports.py                   # Reports and analytics module
├── settings.py                  # System settings module
│
├── setup_database.sql           # Database setup script
├── warehouse_settings.json      # Application settings (auto-generated)
│
├── warehouse_env/               # Virtual environment (if created)
│
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── LICENSE                      # License file
│
└── docs/                        # Additional documentation
    ├── INSTALLATION.md
    ├── USER_GUIDE.md
    └── API.md
```

---

## 🔌 API Reference

### DatabaseConfig Class

```python
from db_config import DatabaseConfig

# Initialize
db = DatabaseConfig()

# Get connection
connection = db.get_connection()

# Verify user
user = db.verify_user(username, password)
# Returns: (id, username, role) or None
```

### Common Database Operations

**Query Products:**
```python
cursor.execute("SELECT * FROM products WHERE quantity > 0")
products = cursor.fetchall()
```

**Insert Order:**
```python
cursor.execute("""
    INSERT INTO orders (customer_name, total_amount, status, order_date)
    VALUES (%s, %s, %s, %s)
""", (customer_name, total, 'Pending', datetime.now()))
order_id = cursor.lastrowid
```

**Update Product Quantity:**
```python
cursor.execute("""
    UPDATE products SET quantity = quantity - %s WHERE id = %s
""", (quantity, product_id))
connection.commit()
```

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Python not found"
**Solution:**
```bash
# Windows: Reinstall Python with "Add to PATH" checked
# Or add Python to PATH manually:
setx PATH "%PATH%;C:\Python39"

# Verify:
python --version
```

#### Issue 2: "ModuleNotFoundError: No module named 'mysql'"
**Solution:**
```bash
pip install mysql-connector-python
# Or in virtual environment:
warehouse_env\Scripts\activate
pip install mysql-connector-python
```

#### Issue 3: "Access denied for user 'root'@'localhost'"
**Solution:**
```bash
# Update password in db_config.py
# Or reset MySQL root password:
mysql -u root
ALTER USER 'root'@'localhost' IDENTIFIED BY 'newpassword';
FLUSH PRIVILEGES;
```

#### Issue 4: "Can't connect to MySQL server"
**Solution:**
```bash
# Windows: Check MySQL service
# Win + R → services.msc → MySQL80 → Start

# macOS:
brew services start mysql

# Linux:
sudo systemctl start mysql
```

#### Issue 5: "Database 'warehouse_db' doesn't exist"
**Solution:**
```bash
mysql -u root -p < setup_database.sql
```

#### Issue 6: Virtual environment activation error (PowerShell)
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Or switch to CMD:
warehouse_env\Scripts\activate.bat
```

#### Issue 7: "matplotlib not displaying charts"
**Solution:**
```bash
pip install --upgrade matplotlib
# On Linux, also install:
sudo apt-install python3-tk
```

---

## ❓ FAQ

**Q: Can I change the database password after setup?**
A: Yes, update the password in `db_config.py` and ensure it matches your MySQL root password.

**Q: How do I backup my data?**
A: Use Settings → Backup & Restore → Create Backup, or manually export via MySQL:
```bash
mysqldump -u root -p warehouse_db > backup.sql
```

**Q: Can multiple users access the system simultaneously?**
A: This is a desktop application designed for single-user access. For multi-user concurrent access, consider deploying a web-based version.

**Q: How do I add more users?**
A: Login as admin → Settings → Users → Add New User

**Q: Can I customize the currency symbol?**
A: Yes, go to Settings → General → Currency Symbol and choose from available options.

**Q: How do I reset the admin password?**
A: Run this SQL command:
```sql
UPDATE users SET password = 'newpassword' WHERE username = 'admin';
```

**Q: Can I export data to Excel?**
A: Currently supports CSV export. You can open CSV files in Excel.

**Q: Is this system suitable for large warehouses?**
A: This system is optimized for small to medium-sized operations. For enterprise-level requirements, consider scaling to a web-based solution.

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Reporting Bugs

1. Check if the issue already exists in [Issues](https://github.com/Meetrao/WarehouseManagement)/issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - System information (OS, Python version, MySQL version)
   - Screenshots if applicable

### Suggesting Enhancements

1. Open an issue with tag `enhancement`
2. Describe the feature and its benefits
3. Provide examples or mockups if possible

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/warehouse-management-system.git

# Create virtual environment
python -m venv warehouse_env
source warehouse_env/bin/activate  # or warehouse_env\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest black pylint

# Run tests
pytest tests/

# Format code
black .

# Lint code
pylint *.py
```

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Warehouse Management System - Meetrao

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## 🙏 Acknowledgments

- Built with [Tkinter](https://docs.python.org/3/library/tkinter.html)
- Database powered by [MySQL](https://www.mysql.com/)
- Charts generated with [Matplotlib](https://matplotlib.org/)
- Inspired by modern warehouse management needs

---

## 📞 Contact

**Project Maintainer:** Meet Rao

- Email: meetr3258@gmail.com
- GitHub: [@Meetrao](https://github.com/Meetrao)
- LinkedIn: [Meet Rao](www.linkedin.com/in/meet-rao-a99a00276)

**Project Link:** [https://github.com/Meetrao/WarehouseManagement](https://github.com/Meetrao/WarehouseManagement)

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Web-based interface
- [ ] RESTful API
- [ ] Barcode scanning support
- [ ] Email notifications
- [ ] Multi-warehouse support
- [ ] Advanced reporting with PDF export
- [ ] Mobile app companion
- [ ] Integration with popular e-commerce platforms

### Version 1.5 (In Progress)
- [ ] Dark mode theme
- [ ] Print invoice functionality
- [ ] Export to Excel
- [ ] Automated backup scheduling
- [ ] User activity logs

---

## 📊 Version History

### v1.0.0 (Current)
- ✅ Initial release
- ✅ Products management
- ✅ Orders management
- ✅ Suppliers management
- ✅ Reports and analytics
- ✅ User management
- ✅ Settings configuration
- ✅ Database backup/restore


**Made with ❤️ for better warehouse management**

⭐ Star this repo if you find it helpful!

[Report Bug]((https://github.com/Meetrao/WarehouseManagement)/issues) · [Request Feature](https://github.com/Meetrao/WarehouseManagement/issues)

</div>
