// const server = 'https://userstudy.appinventor.mit.edu/api';
const server = 'http://localhost:8080';

const instructions_text = [
    "Begin by typing or saying 'Hello'.",
    "Then, type or say 'Start programming'.",
    "Type or say 'Hello world!'.",
]

const tutorial_required_messages = [
    "Hello",
    "Start programming",
    "Hello world!"
]

socketApi.on('response', (data) => {
    console.log(data)
    addUtter("agent-utter", data.message, data.speak);
})

let tutorial_step = 0;
let tutorial = true;
let voice;

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
    let text = textbox.value;
    if (text != "")
        submitMessage(text.toLowerCase(), false);

    textbox.value = "";
}

let submitMessage = (message, speak) => {
    addUtter("user-utter", message)

    if (tutorial)
        handleTutorial(message, speak);
    else
        handleSubmit(message, speak);
}

let handleTutorial = (message, speak) => {
    let correct = tutorial_required_messages[tutorial_step].toLowerCase().includes(message);

    if (correct)
        tutorial_step++;

    if (message === "skip" || tutorial_step > instructions_text.length - 1) {
        document.getElementById("sidebar-tutorial").style.display = "none";
        document.getElementById("sidebar").style.display = "block";
        tutorial = false;
        addUtter("agent-utter", "You have finished the tutorial!", speak);
        addUtter("agent-utter", "What would you like to do now?", speak);
    } else {
        if (!correct)
            addUtter("agent-utter", "To advance, please follow the instructions on the left.", speak);
        document.getElementById("sidebar-tutorial").innerHTML = `
            <div><b>You are currently in practice mode.</b></div>
            <div>${instructions_text[tutorial_step]}</div><br>
            <div>If you want to skip the tutorial at any time, type or say 'Skip'.</div>
        `
    }
};

let handleSubmit = (message, speak) => {
    socketApi.emit('message', { message: message, sid: localStorage.getItem('sid'), speak: speak })
};

let speakUtter = (message) => {
    let audio = new SpeechSynthesisUtterance(message);
    audio.voice = voice;
    audio.volume = 1;
    audio.rate = 0.9;
    audio.pitch = 1.0;
    audio.lang = 'en-US';
    window.speechSynthesis.speak(audio);
}

let addUtter = (className, message, speak=true) => {
    if (speak && className === "agent-utter")
        speakUtter(message);

    let conversation = document.getElementById("conversation");
    if (conversation != null) {
        let utter = document.createElement("div");
        utter.className = className;

        let text = document.createElement("div");
        text.innerHTML = message;

        utter.append(text);
        conversation.prepend(utter);
    }
};

document.addEventListener("DOMContentLoaded", () => {
    let textbox = document.getElementById("textbox");
    if (textbox != null) {
        textbox.onkeyup = (e) => {
            e.preventDefault();
            if (e.keyCode === 13)
                submitText();
        }
    }

    window.speechSynthesis.onvoiceschanged = () => {
        voice = window.speechSynthesis.getVoices().filter((voice) => {
            return voice.name == 'Google US English';
        })[0];
    };
});

if (checkQuery("tutorial", 0)) {
    document.getElementById("sidebar-tutorial").style.display = "none";
    document.getElementById("sidebar").style.display = "block";
    tutorial = false;
    addUtter("agent-utter", "Hi, what would you like to do?", false);
} else {
    document.getElementById("sidebar-tutorial").innerHTML = `
        <div><b>You are currently in practice mode.</b></div>
        <div>${instructions_text[tutorial_step]}</div><br>
        <div>If you want to skip the tutorial at any time, type or say 'Skip'.</div>`;
    addUtter("agent-utter", "Hi, please follow the instructions on the left.", false);
}
