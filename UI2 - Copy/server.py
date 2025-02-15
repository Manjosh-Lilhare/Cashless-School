from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import time
import random
import os
from threading import Lock

app = Flask(__name__)

# MongoDB connection using environment variable (fallback to hardcoded URI if not set)
MONGO_URI= os.environ.get("MONGO_URI", "mongodb://localhost:27017/db") 

MONGO_URI = os.environ.get("MONGO_URI", "mongodb+srv://lilharemanjosh1:Manjosh2327@cluster0.7zxn5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")    

client = MongoClient(MONGO_URI)
db = client.Canteen_data
orders = db.orders

# Dictionary to store temporary order details and payment statuses
payment_statuses = {}
payment_status_lock = Lock()  # Thread-safe lock for accessing payment_statuses

# Canteen page
@app.route('/')
def canteen():
    return render_template('canteen.html')

# Loading page
@app.route('/loading')
def loading():
    return render_template('loading.html')

# Payment status page
@app.route('/payment_status')
def payment_status():
    return render_template('payment_status.html')

# API to handle order submission
@app.route('/submit_order', methods=['POST'])
def submit_order():
    data = request.json
    selected_products = data.get('products')
    total_price = data.get('total_price')
    order_id = random.randint(1000, 9999)  # Generate a random order ID

    # Simulate payment processing
    time.sleep(5)  # Simulate a 5-second delay
    payment_status = "pending"  # Initial status is pending

    # Store order details along with status
    with payment_status_lock:
        payment_statuses[order_id] = {
            "status": payment_status,
            "products": selected_products,
            "total_price": total_price
        }

    return jsonify({"order_id": order_id, "status": payment_status})

# API to update payment status
@app.route('/update_status/<int:order_id>/<int:response>', methods=['POST'])
def update_status(order_id, response):
    if response == 200:
        status = "success"
    elif response == 404:
        status = "failed"
    else:
        return jsonify({"error": "Invalid response code"}), 400

    # Update the payment status in the dictionary
    with payment_status_lock:
        if order_id in payment_statuses:
            payment_statuses[order_id]["status"] = status
        else:
            return jsonify({"error": "Order ID not found"}), 404

    # Save order to MongoDB only if payment is successful
    if status == "success":
        order_data = {
            "order_id": order_id,
            "products": payment_statuses[order_id]["products"],
            "total_price": payment_statuses[order_id]["total_price"],
            "status": status,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        orders.insert_one(order_data)

    return jsonify({"order_id": order_id, "status": status})

# API to check payment status
@app.route('/check_payment_status/<int:order_id>', methods=['GET'])
def check_payment_status(order_id):
    max_attempts = 10  # Maximum number of attempts to check payment status
    attempt = 0

    while attempt < max_attempts:
        with payment_status_lock:
            if order_id in payment_statuses and payment_statuses[order_id]["status"] != "pending":
                status = payment_statuses[order_id]["status"]
                return jsonify({"status": status, "order_id": order_id})

        attempt += 1
        time.sleep(2)  # Wait for 2 seconds between attempts

    # If no response after max_attempts, return payment failed
    return jsonify({"status": "failed", "order_id": order_id}), 404

if __name__ == '__main__':
    app.run(debug=True)
