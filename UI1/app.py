# Flask Server on Raspberry Pi 5 (Handles Payments & Orders)
from flask import Flask, render_template, request, jsonify, redirect, url_for
from pymongo import MongoClient
import random
import datetime

app = Flask(__name__)

# MongoDB Connection (Replace <db_password> with actual password)
client_local = MongoClient("mongodb+srv://lilharemanjosh1:Manjosh2327@cluster0.7zxn5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db_local = client_local["cashless_school"]
transactions_local = db_local["transactions"]
orders_local = db_local["orders"]

# Additional MongoDB Atlas Connection
client_atlas = MongoClient("mongodb+srv://lilharemanjosh1:Manjosh2327@cluster0.7zxn5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db_atlas = client_atlas["cashless_school"]
transactions_atlas = db_atlas["transactions"]
orders_atlas = db_atlas["orders"]

# Store order status
order_status = {}

# Sample menu items
menu_items = [
    {"id": "1", "name": "Schezwan Margherita", "price": 299},
    {"id": "2", "name": "Farmhouse Pizza", "price": 349},
    {"id": "3", "name": "Cheese Burst Pizza", "price": 399}
]

@app.route('/')
def menu():
    return render_template('menu.html', menu_items=menu_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    selected_items = request.form.getlist('menu_items')
    if not selected_items:
        print("No items selected.")
    else:
        print("Selected Items IDs:", selected_items)  # Debugging output
    
    total_price = sum(int(item['price']) for item in menu_items if str(item['id']) in selected_items)
    order_id = random.randint(1000, 9999)
    order_status[order_id] = "pending"
    
    return redirect(url_for('order_status_page', order_id=order_id, total_price=total_price))

@app.route('/order_status/<int:order_id>/<int:total_price>')
def order_status_page(order_id, total_price):
    return render_template('order_status.html', order_id=order_id, total_price=total_price)

@app.route('/check_status/<int:order_id>', methods=['GET'])
def check_status(order_id):
    status = order_status.get(order_id)
    if status == "pass":
        return jsonify({"status": "pass"})
    return jsonify({"status": "waiting"})

@app.route('/update_status/<int:order_id>', methods=['POST'])
def update_status(order_id):
    if order_id in order_status:
        order_status[order_id] = "pass"
        order_data = {
            "order_id": order_id,
            "status": "pass",
            "timestamp": datetime.datetime.utcnow()
        }
        transactions_local.insert_one(order_data)
        transactions_atlas.insert_one(order_data)
        return jsonify({"message": "Status updated to pass and transaction saved"})
    return jsonify({"status": "not found", "message": "Order ID not found"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
