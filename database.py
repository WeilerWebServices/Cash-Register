"""
SQLite database operations for the cash register system
"""

import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path='cash_register.db'):
        """Initialize database connection and create tables"""
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()
        
    def create_tables(self):
        """Create required tables if they don't exist"""
        # Inventory table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL,
                quantity INTEGER NOT NULL,
                description TEXT,
                barcode TEXT UNIQUE
            )
        ''')
        
        # Customers table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT,
                address TEXT,
                city TEXT,
                state TEXT,
                zip_code TEXT,
                dob TEXT NOT NULL,
                id_image_path TEXT NOT NULL,
                date_added TEXT NOT NULL
            )
        ''')
        
        # Transactions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                total REAL NOT NULL,
                tax REAL NOT NULL,
                payment_method TEXT NOT NULL,
                items TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                id_verified INTEGER NOT NULL,
                FOREIGN KEY(customer_id) REFERENCES customers(id)
            )
        ''')
        self.conn.commit()
    
    # Additional database operations...
    # (Add methods for CRUD operations on all tables)
    
    def close(self):
        """Close database connection"""
        self.conn.close()