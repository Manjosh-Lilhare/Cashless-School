from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
from datetime import datetime
import time
import random

app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb+srv://lilharemanjosh1:Manjosh2327@cluster0.7zxn5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.canteen_db
orders = db.orders

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
    payment_status = "success" if random.choice([True, False]) else "failed"

    # Save order to MongoDB
    if payment_status == "success":
        order_data = {
            "order_id": order_id,
            "products": selected_products,
            "total_price": total_price,
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S")
        }
        orders.insert_one(order_data)

    return jsonify({"order_id": order_id, "status": payment_status})

# API to check payment status
@app.route('/check_payment_status/<int:order_id>', methods=['GET'])
def check_payment_status(order_id):
    order = orders.find_one({"order_id": order_id})
    if order:
        return jsonify({"status": "success", "order_id": order_id})
    else:
        return jsonify({"status": "failed", "order_id": order_id}), 404

if __name__ == '__main__':
    app.run(debug=True)