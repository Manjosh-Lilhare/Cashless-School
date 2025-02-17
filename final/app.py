from flask import Flask, render_template, request, jsonify
import json
import random
import time
from app2 import process_payment  # Import function from app2.py

app = Flask(__name__)

# JSON File Paths
CONFIG_FILE = "config.json"
PURCHASES_FILE = "purchases.json"

# Sample menu items
menu_items = [
    {"id": 1, "name": "Schezwan Margherita", "price": 299},
    {"id": 2, "name": "Farmhouse Pizza", "price": 349},
    {"id": 3, "name": "Cheese Burst Pizza", "price": 399}
]

# Load or Create config.json
default_config = {
    "face_data_file": "face_encodings.pkl",
    "camera_settings": {"timeout": 10},
    "rfid": {"port": "/dev/ttyACM0", "baudrate": 9600, "valid_ids": ["CARD ID: 3660550963"]},
    "fingerprint": {"port": "/dev/ttyUSB0", "baudrate": 57600},
    "orders": {}
}

try:
    with open(CONFIG_FILE, "r") as config_file:
        config = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError):
    print("Creating new config.json...")
    config = default_config
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)

# Load or Create purchases.json
try:
    with open(PURCHASES_FILE, "r") as purchases_file:
        purchases = json.load(purchases_file)
except (FileNotFoundError, json.JSONDecodeError):
    print("Creating new purchases.json...")
    purchases = {"transactions": []}
    with open(PURCHASES_FILE, "w") as purchases_file:
        json.dump(purchases, purchases_file, indent=4)

@app.route('/')
def menu():
    return render_template('menu.html', menu_items=menu_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    selected_items = request.form.getlist('selected_items')
    total_price = sum(item['price'] for item in menu_items if str(item['id']) in selected_items)
    order_id = str(random.randint(1000, 9999))
    
    payment_option = request.form.get('payment_mode', 'rfid')  # Default to 'rfid' if not provided
    time.sleep(1)  # Simulate processing delay
    
    payment_success = process_payment(payment_option, total_price)  # Call payment processing

    # Store order status in config.json
    config["orders"][order_id] = {
        "items": selected_items,
        "total_price": total_price,
        "payment_status": "paid" if payment_success else "failed"
    }
    
    with open(CONFIG_FILE, "w") as config_file:
        json.dump(config, config_file, indent=4)  # Save updated order details

    # Store successful purchases in purchases.json
    if payment_success:
        purchase_record = {
            "order_id": order_id,
            "items": selected_items,
            "total_price": total_price
        }
        purchases["transactions"].append(purchase_record)
        with open(PURCHASES_FILE, "w") as purchases_file:
            json.dump(purchases, purchases_file, indent=4)  # Save updated purchases

        return render_template('success.html', order_id=order_id)
    else:
        return render_template('failure.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)