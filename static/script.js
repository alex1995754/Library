document.getElementById("orderForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const bookId = document.getElementById("book_id").value;
    const quantity = document.getElementById("quantity").value;

    const orderData = {
        book_id: bookId,
        quantity: quantity
    };

    fetch("http://localhost:5000/order", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(orderData)
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("orderStatus").innerHTML = `Order placed: ${data.message}`;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("orderStatus").innerHTML = "There was an error placing the order.";
    });
});