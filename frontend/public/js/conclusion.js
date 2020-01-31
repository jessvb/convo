// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    var finishBtn = document.getElementById('btn-finish');

    finishBtn.addEventListener('click', function () {
        // Log the emails + isAdvanced to the server
        var email = document.getElementById('email-textbox').value;
        var isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;
        console.log("email: " + email);
        console.log("isAdvanced: " + isAdvanced);
        console.error("TODO: @Kevin: Log the emails + isAdvanced to the server");

        // change text to just say thank you
        document.getElementById('info').innerHTML = "<br><h2>Thank you for participating!</h2>";
        document.getElementById('textbox-container').style.display = "none";
        document.getElementById('button-container').style.display = "none";
    });

});