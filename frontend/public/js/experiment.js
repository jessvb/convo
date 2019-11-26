document.addEventListener("DOMContentLoaded", () => {
    let textbox = document.getElementById("textbox");
    if (textbox != null) {
        textbox.onkeyup = (e) => {
            e.preventDefault();
            if (e.keyCode === 13) {
                submitMessage();
            }
        }
    }
});

let submitMessage = () => {
    let text = document.getElementById("textbox").value;
    if (text != "") {
        let utter = document.createElement("div");
        utter.className = "user-utter";

        let message = document.createElement("div");
        message.innerHTML = text;

        utter.append(message);
        document.getElementById("conversation").prepend(utter);
    }

    document.getElementById("textbox").value = "";
}
