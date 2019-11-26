let tutorial_step = 0;
let tutorial = true;

const instructions_text = [
    "Begin by typing 'Hello' in the text box.",
    "Then, type 'Start programming'.",
    "Type 'Hello world!'.",
]

const tutorial_required_messages = [
    "Hello",
    "Start programming",
    "Hello world!"
]

let checkQuery = (field, value) => {
    let url = window.location.href;
    let query = `${field}=${value}`
    if (url.indexOf(`?${query}`) != -1)
        return true;
    else if (url.indexOf(`?${query}`) != -1)
        return true;
    return false
}

let submitMessage = () => {
    let text = document.getElementById("textbox").value;
    if (text != "") {
        let utter = document.createElement("div");
        utter.className = "user-utter";

        let message = document.createElement("div");
        message.innerHTML = text;

        utter.append(message);
        document.getElementById("conversation").prepend(utter);

        if (tutorial)
            handleTutorial(text.toLowerCase());
        else
            handleSubmit(text.toLowerCase());
    }

    document.getElementById("textbox").value = "";
}

let handleTutorial = (text) => {
    if (text === tutorial_required_messages[tutorial_step].toLowerCase())
        tutorial_step++;

    if (tutorial_step > instructions_text.length - 1) {
        document.getElementById("sidebar-tutorial").style.display = "none";
        document.getElementById("sidebar").style.display = "block";
        tutorial = false;
    } else {
        document.getElementById("sidebar-tutorial").innerHTML = `
            <div><b>You are currently in practice mode.</b></div>
            <div>${instructions_text[tutorial_step]}</div>
        `
    }
}

let handleSubmit = (text) => {
    axios.post('http://127.0.0.1:5000/message', {
        message: text
    }).then((res) => {
        let utter = document.createElement("div");
        utter.className = "agent-utter";

        let message = document.createElement("div");
        message.innerHTML = res.data.message;

        utter.append(message);
        document.getElementById("conversation").prepend(utter);
    }).catch((err) => {
        console.log(err);
    })
}

if (checkQuery("tutorial", 0)) {
    document.getElementById("sidebar-tutorial").style.display = "none";
    document.getElementById("sidebar").style.display = "block";
    tutorial = false;
} else {
    document.getElementById("sidebar-tutorial").innerHTML = `
        <div><b>You are currently in practice mode.</b></div>
        <div>${instructions_text[tutorial_step]}</div>
    `
}

document.addEventListener("DOMContentLoaded", () => {
    let textbox = document.getElementById("textbox");
    if (textbox != null) {
        textbox.onkeyup = (e) => {
            e.preventDefault();
            if (e.keyCode === 13)
                submitMessage();
        }
    }
});
