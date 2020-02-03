// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    let finishBtn = document.getElementById('btn-finish');
    finishBtn.onclick = (event) => {
        // Log the emails + isAdvanced to the server
        let email = document.getElementById('email-textbox').value;
        let isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;
        socketApi.emit("email", { "email": email, "advanced": isAdvanced });

        // change text to just say thank you
        document.getElementById('info').innerHTML = "<br><h2>Thank you for participating!</h2>";
        document.getElementById('textbox-container').style.display = "none";
        document.getElementById('button-container').style.display = "none";
    };
});
