// Donation amount
function donateAmount(amount){
    document.getElementById('customAmount').value = amount;
}

function donateCustomAmount(){
    var customAmount = document.getElementById('customAmount').value;

    if (customAmount && !isNaN(customAmount) && parseInt(customAmount) > 0){
        // Confirmation alert
        var confirmDonation = confirm('Are you sure that you want to donate $' + customAmount + '?');

        if (confirmDonation){
            // Clicking on "OK" redirects to the checkout page + passes customAmount
            window.location.href = '/checkout?amount=' + customAmount;
        } else{
            alert('Donation cancelled.');
        }
    } else{
        alert('Please enter a valid donation amount.')
    }
}

// Non-numerical values not allowed in number based form fields
function validateNumericInput(input){
    // Remove non-numeric characters from the input value
    input.value = input.value.replace(/\D/g, '');
}

// Past dates cannot be chosen
document.addEventListener("DOMContentLoaded", function(){
    // Get the DateField element
    var edateInput = document.getElementById("edate");

    // Set the minimum date to today
    var today = new Date().toISOString().split("T")[0]; //ISO 8601 format
    edateInput.setAttribute("min", today);
});