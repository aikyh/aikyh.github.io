// Donation amount
function donateAmount(amount) {
    document.getElementById('customAmount').value = amount;
}

function updateProgress(amount) {
    var progressBar = document.querySelector('.progress-bar');
    var currentAmount = parseFloat(progressBar.style.width) || 0;
    var goalAmount = 1000;
    var newAmount = (currentAmount / 100) * goalAmount + parseFloat(amount);
    var newPercentage = (newAmount / goalAmount) * 100;

    progressBar.style.width = newPercentage + '%';

    // Update the percentage text
    progressBar.innerText = newPercentage.toFixed(2) + '%';

    // Update the raised amount text
    var raisedAmount = document.querySelector('.raised');
    raisedAmount.innerText = '$' + newAmount.toFixed(2) + ' raised out of $' + goalAmount + ' goal';

    // Store progress in cookie
    document.cookie = "progress=" + newAmount;
}

function donateCustomAmount() {
    var customAmount = document.getElementById('customAmount').value;

    if (customAmount && !isNaN(customAmount) && parseInt(customAmount) > 0) {
        // Confirmation alert
        var confirmDonation = confirm('Are you sure that you want to donate $' + customAmount + '?');

        if (confirmDonation) {
            // Clicking on "OK" redirects to the checkout page + passes customAmount
            window.location.href = '/checkout?amount=' + customAmount;

            // Update progress after the donation is confirmed
            updateProgress(customAmount);
        } else {
            alert('Donation cancelled.');
        }
    } else {
        alert('Please enter a valid donation amount.')
    }
}

// Function to retrieve cookie value
function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length == 2) return parts.pop().split(";").shift();
}

// On page load, check for progress cookie and update progress bar
window.onload = function() {
    var progress = getCookie("progress");
    if (progress) {
        updateProgress(parseFloat(progress));
    }
};


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

// Function to filter products based on tag
function filterProducts(tag){
    var rows = document.querySelectorAll('.product-row');
    rows.forEach(function(row){
        var tags = row.getAttribute('data-tags');
        if (tag === 'all' || tags.includes(tag)){
            row.style.display = '';
        } else{
              row.style.display = 'none';
          }
    });
}