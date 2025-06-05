"""
Integration with Shopify for payment processing
"""

import requests
import json

class ShopifyProcessor:
    def __init__(self, api_key, password, store_name):
        """
        Initialize Shopify connection
        :param api_key: Shopify API key
        :param password: Shopify API password
        :param store_name: Shopify store name
        """
        self.api_key = api_key
        self.password = password
        self.store_name = store_name
        self.base_url = f"https://{self.api_key}:{self.password}@{self.store_name}.myshopify.com/admin/api/2023-07"
        
    def process_payment(self, amount, items, customer_info=None):
        """
        Process a payment through Shopify
        :param amount: Total amount to charge
        :param items: List of items in transaction
        :param customer_info: Optional customer information
        :return: Tuple of (success: bool, transaction_id: str)
        """
        try:
            # Create order
            order_data = {
                "order": {
                    "line_items": items,
                    "total_price": str(amount),
                    "financial_status": "paid"
                }
            }
            
            if customer_info:
                order_data["order"]["customer"] = customer_info
            
            response = requests.post(
                f"{self.base_url}/orders.json",
                json=order_data,
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 201:
                order_id = response.json()["order"]["id"]
                return True, order_id
            return False, None
            
        except Exception as e:
            print(f"Payment processing error: {e}")
            return False, None