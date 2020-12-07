// Connect to Convo server on production
// const server = 'https://userstudy.appinventor.mit.edu/api';
// Connect to Convo server on local
const server = 'http://localhost:5000';

const synth = window.speechSynthesis;
synth.cancel();
let state = "home";

const action_commands = [{
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
            "add 5 to variable foo",
            "add to foo"
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
            "if foo is greater than 5, say hooray",
            "if bar is less than 10, add 10 to variable bar"
        ]
    },
    {
        "title": "Make a While Loop",
        "examples": [
            "while foo is less than 2, add 2 to variable foo",
            "make a while loop"
        ]
    },
    {
        "title": "Make a Until Loop",
        "examples": [
            "add 2 to variable foo until foo is equal to 20",
            "make an until loop"
        ]
    },
    {
        "title": "Give a Condition (Only When Asked)",
        "examples": [
            "if foo is equal to 5",
            "until foo is greater than 2",
            "while foo is not 0"
        ]
    },
    {
        "title": "Get User Input",
        "examples": [
            "get user input",
            "get user input and call it foo"
        ]
    },
    {
        "title": "Cancel the Current Action",
        "examples": [
            "cancel"
        ]
    }
]

const example_commands = {
    "home": [{
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
    "creating": [{
        "title": "Finish Creating",
        "examples": [
            "done"
        ]
    }].concat(action_commands),
    "editing_action": action_commands,
    "editing": [
        {
            "title": "Finish Editing Procedure or Leave Loop",
            "examples": [
                "done"
            ]
        },
        {
            "title": "Navigate Through Procedure",
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
                "add step",
                "make a new step",
                "create a new step"
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
        },
        {
            "title": "Step Into Loop",
            "examples": [
                "step into"
            ]
        }
    ].concat(action_commands),
    "executing": [{
        "title": "Stop Currently Running Procedure",
        "examples": [
            "stop",
            "cancel"
        ]
    }]
}

let handleStateChange = (newState) => {
    state = newState;
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
        if ('state' in data)
            handleStateChange(data.state);
        addUtter("agent-utter", data.message, data.speak);
    }
}

socketApi.on('response', handleSocketApiResponse);

socketApi.on('trained', () => {
    let nluContainer = document.getElementById('nlu-container');
    let doneTraining = document.createElement('div');
    let text = document.createElement('div');
    text.innerHTML = "Done Training";

    doneTraining.append(text);
    nluContainer.append(doneTraining);
});

socketApi.on('playSound', (data) => {
    let audioPlayer = document.getElementById('audio-player');
    audioPlayer.src = `assets/${data.sound}.mp3`;
    addUtter("agent-utter", `Playing ${data.sound} sound.`, false);
    audioPlayer.play();
});

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
    if (text != "") {
        synth.cancel();
        submitMessage(text.toLowerCase(), false);
    }

    textbox.value = "";
}

let trainNLU = () => {
    let intentElements = document.getElementsByClassName("intent");
    let trainingElements = document.getElementsByClassName("training");
    let intents = [];
    let trainingData = [];
    for (var i=0; i < intentElements.length; i++) {
        let intent = intentElements[i].value;
        if (intent != "") {
            intents.push(intent);
            trainingData.push(trainingElements[i].value);
        }
    }
    if (intents != []) {
        socketApi.emit('train', {
            intents: intents,
            trainingData: trainingData,
        })
    }
}

let addIntent = () => {
    let nluContainer = document.getElementById('nlu');
    let newIntent = document.createElement('div');
    newIntent.innerHTML = `<div><b>INTENT</b>: What do you want Convo to understand?</div>
    <input class="intent" type="text" id="intent" placeholder="keep a recipe book"/>`;
    let newTrainingData = document.createElement('div');
    newTrainingData.innerHTML = `<div><b>TRAINING DATA</b>: How might you say this?</div>
    <input class="training" type="text" id="training_data" placeholder="I want to save a recipe"/>`;
    nluContainer.append(newIntent);
    nluContainer.append(newTrainingData);
}

let submitMessage = (message, speak) => {
    addUtter("user-utter", message);
    handleSubmit(message, speak);
}

let handleSubmit = (message, speak) => {
    if (state === "executing" && message.toLowerCase().trim() === "stop")
        synth.cancel();
    socketApi.emit('message', {
        message: message,
        sid: localStorage.getItem('sid'),
        speak: speak,
        isUnconstrained: document.getElementById("switchValue").checked
    })
};

let speakUtter = (message) => {
    let audio = new SpeechSynthesisUtterance(message);
    audio.voice = synth.getVoices().filter((voice) => {
        return voice.name == 'Google US English' || voice.name == 'Samantha';
    })[0];
    audio.volume = 1;
    audio.rate = 0.9;
    audio.pitch = 1.0;
    audio.lang = 'en-US';
    synth.speak(audio);
}

let addUtter = (className, message, speak = true) => {
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

let addExampleActions = () => {
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

    handleStateChange("home");
}

let addAudioPlayer = () => {
    let audioPlayer = document.createElement('audio');
    audioPlayer.id = 'audio-player';
    audioPlayer.preload = 'none';
    audioPlayer.style = "display: none";
    document.body.appendChild(audioPlayer);

    synth.onvoiceschanged = () => {
        voice = synth.getVoices().filter((voice) => {
            return voice.name == 'Google US English' || voice.name == 'Samantha';
        })[0];
    };
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

    let exampleActions = document.getElementById('example-actions');
    if (exampleActions != null) {
        addExampleActions();
    }

    let examplePrograms = document.getElementById('example-programs');
    if (examplePrograms != null) {
        addExamplePrograms();
    }

    addAudioPlayer();
});
