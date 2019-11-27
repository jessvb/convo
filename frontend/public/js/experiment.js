const server = 'http://0.0.0.0:5000/message';
// const server = 'http://3.87.219.25:5000/message';
// const server = 'https://0.0.0.0:5000/message';
// const server = 'https://3.87.219.25:5000/message';

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

let tutorial_step = 0;
let tutorial = true;

let checkQuery = (field, value) => {
    let url = window.location.href;
    let query = `${field}=${value}`
    if (url.indexOf(`?${query}`) != -1)
        return true;
    else if (url.indexOf(`?${query}`) != -1)
        return true;
    return false
}

let submitText = () => {
    let textbox = document.getElementById("textbox");
    let text = textbox.value
    if (text != "")
        submitMessage(text.toLowerCase());

    textbox.value = "";
}

let submitMessage = (message) => {
    let utter = document.createElement("div");
    utter.className = "user-utter";

    let text = document.createElement("div");
    text.innerHTML = message;
     utter.append(text);

    let conversation = document.getElementById("conversation");
    if (conversation != null)
        conversation.prepend(utter);

    if (tutorial)
        handleTutorial(message);
    else
        handleSubmit(message);
}

let handleTutorial = (message) => {
    if (tutorial_required_messages[tutorial_step].toLowerCase().includes(message))
        tutorial_step++;

    if (tutorial_step > instructions_text.length - 1) {
        document.getElementById("sidebar-tutorial").style.display = "none";
        document.getElementById("sidebar").style.display = "block";
        tutorial = false;
    } else
        document.getElementById("sidebar-tutorial").innerHTML = `
            <div><b>You are currently in practice mode.</b></div>
            <div>${instructions_text[tutorial_step]}</div>
        `
};

let handleSubmit = (message) => {
    axios.post(server, { message: message})
        .then((res) => {
            let utter = document.createElement("div");
            utter.className = "agent-utter";

            let text = document.createElement("div");
            text.innerHTML = res.data.message;

            utter.append(text);
            document.getElementById("conversation").prepend(utter);
        })
        .catch(console.log);
};

if (checkQuery("tutorial", 0)) {
    document.getElementById("sidebar-tutorial").style.display = "none";
    document.getElementById("sidebar").style.display = "block";
    tutorial = false;
} else {
    document.getElementById("sidebar-tutorial").innerHTML = `
        <div><b>You are currently in practice mode.</b></div>
        <div>${instructions_text[tutorial_step]}</div>`;
}

document.addEventListener("DOMContentLoaded", () => {
    let textbox = document.getElementById("textbox");
    if (textbox != null) {
        textbox.onkeyup = (e) => {
            e.preventDefault();
            if (e.keyCode === 13)
                submitText();
        }
    }
});
