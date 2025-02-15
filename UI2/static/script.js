let cart = [];
let totalPrice = 0;

function addToCart(name, price) {
    cart.push({ name, price });
    totalPrice += price;
    updateCart();
}

function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const totalPriceElement = document.getElementById('total-price');
    cartItems.innerHTML = '';
    cart.forEach(item => {
        const li = document.createElement('li');
        li.textContent = `${item.name} - $${item.price.toFixed(2)}`;
        cartItems.appendChild(li);
    });
    totalPriceElement.textContent = totalPrice.toFixed(2);
}

async function proceedToPayment() {
    const response = await fetch('/submit_order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ products: cart, total_price: totalPrice })
    });
    const data = await response.json();
    window.location.href = `/loading?order_id=${data.order_id}`;
}

// Check payment status on loading page
async function checkPaymentStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const orderId = urlParams.get('order_id');
    const response = await fetch(`/check_payment_status/${orderId}`);
    if (response.ok) {
        const data = await response.json();
        if (data.status === 'success') {
            window.location.href = `/payment_status?order_id=${orderId}&status=success`;
        } else {
            window.location.href = `/payment_status?order_id=${orderId}&status=failed`;
        }
    }
}

// Display payment status on payment_status page
function displayPaymentStatus() {
    const urlParams = new URLSearchParams(window.location.search);
    const status = urlParams.get('status');
    const statusMessage = document.getElementById('status-message');
    if (status === 'success') {
        statusMessage.textContent = 'Payment Successful! Thank you for your order.';
    } else {
        statusMessage.textContent = 'Payment Failed. Please try again.';
    }
}

// Run appropriate function based on the current page
if (window.location.pathname === '/loading') {
    checkPaymentStatus();
} else if (window.location.pathname === '/payment_status') {
    displayPaymentStatus();
}