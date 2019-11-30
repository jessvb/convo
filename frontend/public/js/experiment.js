const server = 'http://0.0.0.0:5000';

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
    addUtter("user-utter", message)

    if (tutorial)
        handleTutorial(message);
    else
        handleSubmit(message);
}

let handleTutorial = (message) => {
    if (tutorial_required_messages[tutorial_step].toLowerCase().includes(message))
        tutorial_step++;

    if (message === "skip" || tutorial_step > instructions_text.length - 1) {
        document.getElementById("sidebar-tutorial").style.display = "none";
        document.getElementById("sidebar").style.display = "block";
        tutorial = false;
        addUtter("agent-utter", "You have finished the tutorial!");
        addUtter("agent-utter", "What would you like to do now?");
    } else {
        addUtter("agent-utter", "To advance, please follow the instructions on the left.");
        document.getElementById("sidebar-tutorial").innerHTML = `
            <div><b>You are currently in practice mode.</b></div>
            <div>${instructions_text[tutorial_step]}</div>
        `
    }
};

let handleSubmit = (message) => {
    axios.post(`${server}/message`, { message: message, clientId: localStorage.getItem("clientId") })
        .then((res) => addUtter("agent-utter", res.data.message))
        .catch(console.log);
};

let addUtter = (className, message) => {
    let utter = document.createElement("div");
    utter.className = className;

    let text = document.createElement("div");
    text.innerHTML = message;

    utter.append(text);

    let conversation = document.getElementById("conversation");
    if (conversation != null)
        conversation.prepend(utter);
};

if (checkQuery("tutorial", 0)) {
    document.getElementById("sidebar-tutorial").style.display = "none";
    document.getElementById("sidebar").style.display = "block";
    tutorial = false;
    addUtter("agent-utter", "Hi, what would you like to do?");
} else {
    document.getElementById("sidebar-tutorial").innerHTML = `
        <div><b>You are currently in practice mode.</b></div>
        <div>${instructions_text[tutorial_step]}</div>`;
    addUtter("agent-utter", "Hi, please follow the instructions on the left.")
    addUtter("agent-utter", "If you want to skip the tutorial at any time, type 'Skip'.")
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

    axios.post(`${server}/reset`, { clientId: localStorage.getItem("clientId") })
        .catch(console.log);
});
