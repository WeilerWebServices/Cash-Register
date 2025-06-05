"""
Data export functionality (Excel, CSV, etc.)
"""

import pandas as pd
from datetime import datetime

class DataExporter:
    @staticmethod
    def to_excel(db_conn, file_path):
        """
        Export all data to an Excel file with multiple sheets
        :param db_conn: Database connection
        :param file_path: Path to save Excel file
        :return: True if successful, False otherwise
        """
        try:
            with pd.ExcelWriter(file_path) as writer:
                # Export transactions
                pd.read_sql_query("SELECT * FROM transactions", db_conn).to_excel(
                    writer, sheet_name='Transactions', index=False)
                
                # Export inventory
                pd.read_sql_query("SELECT * FROM inventory", db_conn).to_excel(
                    writer, sheet_name='Inventory', index=False)
                
                # Export customers (without ID images)
                pd.read_sql_query('''
                    SELECT id, first_name, last_name, email, phone, 
                           address, city, state, zip_code, dob, date_added
                    FROM customers
                ''', db_conn).to_excel(writer, sheet_name='Customers', index=False)
            
            return True
        except Exception as e:
            print(f"Export error: {e}")
            return False