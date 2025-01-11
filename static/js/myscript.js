jQuery.noConflict();
jQuery(document).ready(function($) {
    // Increase quantity handler
    $(document).on('click', '.increase-quantity', function(event) {
        event.preventDefault();
        
        var productId = $(this).data('product-id');
        var quantityElement = document.getElementById('quantity-' + productId);

        $.ajax({
            type: 'GET',
            url: '/pluscart',
            data: { prod_id: productId },
            success: function(data) {
                console.log("data =", data);
                quantityElement.innerText = data.quantity;
                document.getElementById('amount').innerText = data.amount;
                document.getElementById('totalamount').innerText = data.totalamount;
            },
            error: function(error) {
                console.log("Error updating quantity:", error);
            }
        });
    });

    // Decrease quantity handler
    $(document).on('click', '.decrease-quantity', function(event) {
        event.preventDefault();
        
        var productId = $(this).data('product-id');
        var quantityElement = document.getElementById('quantity-' + productId);

        $.ajax({
            type: 'GET',
            url: '/minuscart',
            data: { prod_id: productId },
            success: function(data) {
                console.log("Server response:", data);
                quantityElement.innerText = data.quantity;
                document.getElementById('amount').innerText = data.amount;
                document.getElementById('totalamount').innerText = data.totalamount;
            },
            error: function(error) {
                console.log("Error updating quantity:", error);
            }
        });
    });
});

jQuery.noConflict();
jQuery(document).ready(function($) {
    $(document).on('click', '.remove-item', function(event) {
        event.preventDefault();

        var productId = $(this).data('product-id');
        var itemRow = $(this).closest('.list-group-item'); // Ensure this targets the correct item container

        $.ajax({
            type: 'GET',
            url: "/removecart",
            data: { prod_id: productId },
            success: function(data) {
                console.log("Item removed successfully", data);

                // Remove the entire item row from the DOM
                itemRow.remove();

                // Update total amount if applicable
                $('#totalamount').text("Rs. " + data.totalamount);
                $('#amount').text("Rs. " + data.amount);
            },
            error: function(error) {
                console.log("Error removing item:", error);
            }
        });
    });
});


document.getElementById('addAddressButton').addEventListener('click', function() {
    var newAddressForm = document.getElementById('newAddressForm');
    if (newAddressForm.style.display === "none") {
        newAddressForm.style.display = "block";
        this.textContent = "Hide Address Form";  // Change button text
    } else {
        newAddressForm.style.display = "none";
        this.textContent = "Add New Address";  // Change button text back
    }
});