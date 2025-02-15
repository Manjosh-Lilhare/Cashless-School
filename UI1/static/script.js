document.addEventListener("DOMContentLoaded", function () {
    let totalPrice = 0;
    const invoiceList = document.getElementById("invoice-list");
    const totalPriceElement = document.getElementById("total-price");
    const totalPriceHidden = document.getElementById("total-price-hidden"); // Hidden input field
    const addButtons = document.querySelectorAll(".add-btn");

    addButtons.forEach(button => {
        button.addEventListener("click", function () {
            const card = this.closest(".card");
            const itemName = card.dataset.name;
            const itemPrice = parseInt(card.dataset.price);

            // Add item to invoice list
            const listItem = document.createElement("li");
            listItem.textContent = `${itemName} - ₹${itemPrice}`;
            invoiceList.appendChild(listItem);

            // Update total price
            totalPrice += itemPrice;
            totalPriceElement.textContent = totalPrice;
            totalPriceHidden.value = totalPrice; // Update hidden input field
        });
    });

    // Payment mode update
    const paymentRadios = document.querySelectorAll("input[name='payment_mode']");
    const paymentModeHidden = document.getElementById("payment_mode");

    paymentRadios.forEach(radio => {
        radio.addEventListener("change", function () {
            paymentModeHidden.value = this.value;
        });
    });
});
