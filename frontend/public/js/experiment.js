const server = 'https://userstudy.appinventor.mit.edu/api';

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

const action_commands = [
    {
        "title": "Create a Variable",
        "examples": [
            "create a variable called foo",
            "make a variable"
        ]
    },
    {
        "title": "Set a Variable",
        "examples": [
            "set a variable",
            "set the variable foo to 5"
        ]
    },
    {
        "title": "Add to a (Number) Variable",
        "examples": [
            "add to variable",
            "add 5 to variable foo"
        ]
    },
    {
        "title": "Make Me Say Something",
        "examples": [
            "say 'Hello world!'",
            "say the value of the variable foo"
        ]
    },
    {
        "title": "Make a Conditional",
        "examples": [
            "if foo is greater than 5 then say hooray",
            "if bar is less than 10 then add 10 to variable bar"
        ]
    },
    {
        "title": "Make a While Loop",
        "examples": [
            "while foo is less than 2 then add 2 to variable foo"
        ]
    },
    {
        "title": "Make a Until Loop",
        "examples": [
            "add 2 to variable foo until foo is equal to 20"
        ]
    },
    {
        "title": "Get User Input",
        "examples": [
            "get user input",
            "get user input and call it foo"
        ]
    }
]

const example_commands = {
    "home": [
        {
            "title": "Create a Procedure or Program",
            "examples": [
                "create a procedure",
                "make a procedure called test"
            ]
        },
        {
            "title": "Run a Procedure or Program",
            "examples": [
                "run test"
            ]
        },
        {
            "title": "Edit a Procedure or Program",
            "examples": [
                "edit test",
                "open test"
            ]
        },
        {
            "title": "Rename a Procedure or Program",
            "examples": [
                "rename hello",
                "rename test to hello"
            ]
        },
        {
            "title": "Delete a Procedure or Program",
            "examples": [
                "delete hello"
            ]
        }
    ],
    "creating": action_commands,
    "editing_action": action_commands,
    "editing": [
        {
            "title": "Navigation",
            "examples": [
                "next step",
                "previous step",
                "go to step 5",
                "go to the first step",
                "go to the last step"
            ]
        },
        {
            "title": "Add a New Action",
            "examples": [
                "add step"
            ]
        },
        {
            "title": "Delete Current Action",
            "examples": [
                "remove step",
                "delete step"
            ]
        },
        {
            "title": "Change or Replace Current Action",
            "examples": [
                "change step",
                "replace step"
            ]
        }
    ].concat(action_commands)
}

let changeSidebarText = (state) => {
    let examples = document.getElementById('example-actions-list');
    examples.innerHTML = "";
    if (state != null && state in example_commands) {
        let commands = example_commands[state];
        commands.forEach(action => {
            let node = document.createElement('div');
            node.className = "example-action"
            node.innerHTML = `<div class="action-title"><b>${action.title}</b></div>`;
            action.examples.forEach(ex => {
                node.innerHTML += `<div class="action-example"><em>${ex}</em></div>`;
            })
            examples.appendChild(node);
        })
    }
}

let handleSocketApiResponse = (data) => {
    let audioPlayer = document.getElementById('audio-player');
    if (audioPlayer.src && !audioPlayer.ended) {
        setTimeout(() => handleSocketApiResponse(data), 500);
    } else {
        changeSidebarText(data.state);
        addUtter("agent-utter", data.message, data.speak);
    }
}

socketApi.on('response', handleSocketApiResponse);

socketApi.on('playSound', (data) => {
    let audioPlayer = document.getElementById('audio-player');
    audioPlayer.src = `assets/${data.sound}.mp3`;
    audioPlayer.play();
});

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
        document.getElementById("sidebar").style.display = "flex";
        tutorial = false;
        addUtter("agent-utter", "You have finished the tutorial!", speak);
        addUtter("agent-utter", "What would you like to do now?", speak);
    } else {
        if (!correct)
            addUtter('agent-utter', 'To advance, please follow the instructions on the left.', speak);
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
    audio.voice = window.speechSynthesis.getVoices().filter((voice) => {
        return voice.name == 'Google US English' || voice.name == 'Samantha';
    })[0];
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
        conversation.append(utter);
        conversation.scrollTop = conversation.scrollHeight;
    }
};

let addExamplePrograms = () => {
    let programs = document.getElementById('example-programs-list');
    programs.innerHTML = `
        <div class="example-program">
            <div class="program-title"><b>Hello World!</b></div>
            <ol class="program-instructions">
                <li>Say <em>"Create a procedure called hello"</em></li>
                <li>Say <em>"Say hello world"</em></li>
                <li>Say <em>"Done"</em></li>
                <li>Say <em>"Run hello"</em></li>
            </ol>
        <div>`;
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

    document.getElementById('example-actions').innerHTML = `
        <div id="example-actions-heading">
            <div><b>Things You Can Say To...</b></div>
            <div id="example-actions-direction">&#9660</div>
        </div>
        <div id="example-actions-list"></div>`;
    document.getElementById('example-actions-heading').onclick = () => {
        let actionsList = document.getElementById('example-actions-list');
        let displ = actionsList.style.display === 'block' ? 'none' : 'block';
        document.getElementById('example-actions-direction').innerHTML = displ === 'none' ? "&#9660" : "&#9650";
        actionsList.style.display = displ;
    }
    changeSidebarText("home");

    document.getElementById('example-programs').innerHTML = `
        <div id="example-programs-heading">
            <div><b>Example Programs</b></div>
            <div id="example-programs-direction">&#9660</div>
        </div>
        <div id="example-programs-list"></div>`;

    document.getElementById('example-programs-heading').onclick = () => {
        let programsList = document.getElementById('example-programs-list');
        let displ = programsList.style.display === 'block' ? 'none' : 'block';
        document.getElementById('example-programs-direction').innerHTML = displ === 'none' ? "&#9660" : "&#9650";
        programsList.style.display = displ;
    }
    addExamplePrograms();

    let audioPlayer = document.createElement('audio');
    audioPlayer.id = 'audio-player';
    audioPlayer.preload = 'none';
    audioPlayer.style = "display: none";
    document.body.appendChild(audioPlayer);

    window.speechSynthesis.onvoiceschanged = () => {
        voice = window.speechSynthesis.getVoices().filter((voice) => {
            return voice.name == 'Google US English' || voice.name == 'Samantha';
        })[0];
    };
});

if (checkQuery("tutorial", 0)) {
    document.getElementById("sidebar-tutorial").style.display = "none";
    document.getElementById("sidebar").style.display = "flex";
    tutorial = false;
    addUtter("agent-utter", "Hi, what would you like to do? You can create a procedure or run one you have already created.", false);
} else {
    document.getElementById("sidebar-tutorial").innerHTML = `
        <div><b>You are currently in practice mode.</b></div>
        <div>${instructions_text[tutorial_step]}</div><br>
        <div>If you want to skip the tutorial at any time, type or say 'Skip'.</div>`;
    addUtter("agent-utter", "Hi, please follow the instructions on the left.", false);
}
