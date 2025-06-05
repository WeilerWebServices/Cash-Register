"""
Main application entry point with configuration support
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from database import Database
from camera import CameraHandler
from shopify_integration import ShopifyProcessor
from config.config_handler import ConfigHandler
from models.customer import Customer
from models.inventory import Inventory
from models.transaction import Transaction

class CashRegisterApp(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load configuration
        try:
            self.config = ConfigHandler()
        except Exception as e:
            QMessageBox.critical(None, "Configuration Error", str(e))
            sys.exit(1)
            
        # Verify required directories exist
        self._verify_directories()
        
        # Initialize application
        self.setWindowTitle("Advanced Cash Register System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize components with config
        self.init_components()
        
        # Setup UI
        self.setup_ui()
        
    def _verify_directories(self):
        """Ensure required directories exist"""
        os.makedirs(self.config.get('app.id_image_dir'), exist_ok=True)
        os.makedirs('config', exist_ok=True)
        
    def init_components(self):
        """Initialize application components with configuration"""
        # Database
        db_file = self.config.get('app.database_file')
        self.db = Database(db_path=db_file)
        
        # Camera
        self.camera = CameraHandler()
        
        # Shopify
        shopify_config = self.config.get_shopify_config()
        self.shopify = ShopifyProcessor(
            api_key=shopify_config.get('api_key'),
            password=shopify_config.get('password'),
            store_name=shopify_config.get('store_name')
        )
        
        # Models
        self.customer_model = Customer(self.db)
        self.inventory_model = Inventory(self.db)
        self.transaction_model = Transaction(self.db)
        
    def setup_ui(self):
        """Create and arrange all GUI components"""
        # (Previous UI setup code remains the same)
        # ...
        
    def closeEvent(self, event):
        """Clean up resources when closing"""
        self.camera.release()
        self.db.close()
        event.accept()

if __name__ == "__main__":
    # Check if config file exists, create default if not
    if not os.path.exists('config/config.json'):
        try:
            os.makedirs('config', exist_ok=True)
            with open('config/config.json', 'w') as f:
                default_config = {
                    "shopify": {
                        "api_key": "your_shopify_api_key",
                        "password": "your_shopify_api_password",
                        "store_name": "your-store-name"
                    },
                    "app": {
                        "tax_rate": 0.08,
                        "id_image_dir": "id_images/",
                        "database_file": "cash_register.db",
                        "min_age": 21
                    }
                }
                json.dump(default_config, f, indent=4)
            QMessageBox.information(
                None, 
                "Configuration Created", 
                "A default config file was created at 'config/config.json'. "
                "Please update it with your actual credentials before running the application."
            )
            sys.exit(0)
        except Exception as e:
            QMessageBox.critical(
                None, 
                "Error", 
                f"Could not create config file: {str(e)}"
            )
            sys.exit(1)
    
    # Run application
    app = QApplication(sys.argv)
    window = CashRegisterApp()
    window.show()
    sys.exit(app.exec_())