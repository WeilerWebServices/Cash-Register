"""
Customer data model and operations
"""

from datetime import datetime

class Customer:
    def __init__(self, db):
        """
        Initialize customer model with database connection
        :param db: Database connection object
        """
        self.db = db
        
    def create(self, first_name, last_name, email, dob, id_image_path, **kwargs):
        """
        Create a new customer record
        :param first_name: Customer first name
        :param last_name: Customer last name
        :param email: Customer email
        :param dob: Date of birth (YYYY-MM-DD)
        :param id_image_path: Path to stored ID image
        :param kwargs: Additional optional fields
        :return: Customer ID if successful, None otherwise
        """
        try:
            self.db.cursor.execute('''
                INSERT INTO customers (
                    first_name, last_name, email, dob, id_image_path, date_added,
                    phone, address, city, state, zip_code
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                first_name, last_name, email, dob, id_image_path, datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                kwargs.get('phone'), kwargs.get('address'), kwargs.get('city'),
                kwargs.get('state'), kwargs.get('zip_code')
            ))
            self.db.conn.commit()
            return self.db.cursor.lastrowid
        except Exception as e:
            print(f"Error creating customer: {e}")
            return None
    
    # Additional customer operations...
    # (Add methods for finding, updating, and deleting customers)