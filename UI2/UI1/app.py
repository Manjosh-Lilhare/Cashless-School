from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid

app = Flask(__name__)

# Store order status
order_status = {}

# Sample menu items
menu_items = [
    {"id": 1, "name": "Schezwan Margherita", "price": 299},
    {"id": 2, "name": "Farmhouse Pizza", "price": 349},
    {"id": 3, "name": "Cheese Burst Pizza", "price": 399}
]

@app.route('/')
def menu():
    return render_template('menu.html', menu_items=menu_items)

@app.route('/checkout', methods=['POST'])
def checkout():
    selected_items = request.form.getlist('selected_items')  # Get selected items from form
    total_price = sum(item['price'] for item in menu_items if str(item['id']) in selected_items)

    order_id = str(uuid.uuid4())  # Generate unique order ID
    order_status[order_id] = "pending"

    return redirect(url_for('order_status_page', order_id=order_id, total_price=total_price))

@app.route('/order_status/<order_id>/<int:total_price>')
def order_status_page(order_id, total_price):
    return render_template('order_status.html', order_id=order_id, total_price=total_price)

@app.route('/check_status/<order_id>', methods=['GET'])
def check_status(order_id):
    status = order_status.get(order_id, "not found")
    return jsonify({"status": status})

@app.route('/update_status/<order_id>', methods=['POST'])
def update_status(order_id):
    if order_id in order_status:
        order_status[order_id] = "completed"
        return jsonify({"message": "Status updated to completed"})
    return jsonify({"status": "not found", "message": "Order ID not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
