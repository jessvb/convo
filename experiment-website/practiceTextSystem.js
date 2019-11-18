function enterText() {
    var str = document.getElementById("textbox").value;
    document.getElementById("textbox").value = "";
    var transcript = document.getElementById("transcript").innerHTML;
    document.getElementById("transcript").innerHTML = str + "<br>" + transcript;
}

function reset() {
    document.getElementById("transcript").innerHTML = "";
}