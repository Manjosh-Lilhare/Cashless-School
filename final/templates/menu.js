
    document.addEventListener("DOMContentLoaded", function () {
        let totalPrice = 0;
        const invoiceList = document.getElementById("invoice-list");
        const totalPriceElement = document.getElementById("total-price");

        document.querySelectorAll(".add-btn").forEach(button => {
            button.addEventListener("click", function () {
                const card = this.closest(".card");
                const itemName = card.querySelector("h4").textContent;
                const itemPrice = parseInt(card.querySelector(".price").textContent.replace("₹", ""));

                // Create list item with remove button
                const listItem = document.createElement("li");
                listItem.innerHTML = `${itemName} - ₹${itemPrice} <button class="remove-btn">❌</button>`;
                
                // Append to invoice list
                invoiceList.appendChild(listItem);

                // Update total price
                totalPrice += itemPrice;
                totalPriceElement.textContent = totalPrice;

                // Add event listener to remove item
                listItem.querySelector(".remove-btn").addEventListener("click", function () {
                    listItem.remove();
                    totalPrice -= itemPrice;
                    totalPriceElement.textContent = totalPrice;
                });
            });
        });
    });

