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

const example_analysis_tutorial_commands = {
    "home": [{
            "title": "Create a Procedure or Program",
            "help": `First, you will need to create a procedure. <br>
            <b>CT Skill “Sequences</b>”: Keep in mind that as you are coding, things happen in order. So if your method has steps a, b, c, d, it will run in that order.
            `,
            "examples": [
                "create a procedure",
                "make a procedure called AskForCompliment"
            ]
        },
        {
            "title": "Get User Input to ask for a compliment and give it a name so we can analyze it later on",
            "help": `Next, to interact with the user to see which phrase they want to analyze the toxicity of,
            ask the user for their input. Then, store their input in a variable so that we can analyze it in the next step!
            `,
            "examples": [
                "get user input",
                "get user input and call it userinput"
            ]
        },
        {
            "title": "Analyze the Phrase - Note that analyze a phrase creates a variable <i>toxvar</i> to store the toxicity score",
            "help": `
            <b>CT Skill “data”:</b> 
            Understand how machines learn from a ton of data. It might be interesting to introduce different machine models here and how data is trained / learned from
            <br>Teach students about ethics of bias: how ML can be biased due to the dataset it was trained on
            <br>Find examples of when the model incorrectly classifies something as toxic / not toxic
            <br>Store the user input toxicity probability
            <br>Introduce the ethics of AI model correctness. Is this model always correct?
            `,
            "examples": [
                "analyze the value of the variable userinput"
            ]
        },
        {
            "title": "Make a While Loop",
            "help": `
            <b>CT Skill “conditionals”:</b> 
            Our computer needs out if a sentence is toxic and what to do after that
            <br >Introduce the ethics of a “cutoff score” 
            <br> When should something be classified as toxic? Should it be above 50%? Should we be more careful and classify things as toxic more often? Or should we classify things as toxic less often? (false negatives vs false positives)
            <br> Does it differ based on the application you’re creating?
            `,
            "examples": [
                "make a while loop"
            ]
        },
        {
            "title": "Give while loop conditions",
            "help": `
            <i>While</i> the probability is high, then ask the user to enter something else that’s nicer
            `,
            "examples": [
                "while toxvar is greater than 0.5",
            ]
        },
        {
            "title": "Give next steps in loop conditions",
            "help": `
            <i>While</i> the probability is high, then ask the user to enter something else that’s nicer
            `,
            "examples": [
                "say 'Your phrase is not nice enough. Enter a new one.'",
                "get user input and call it userinput",
                "analyze the value of the variale userinut",
            ]
        },
        {
            "title": "Close the loop",
            "help": `We are done with the loop, so close it now! We have outlined everything that will happen
            while the toxicity score is high."
            `,
            "examples": [
                "close loop",
            ]
        },
        {
            "title": "Make Me Say Something",
            "help" : `Have the program let the user know what the compliment was! After all, we are asking for compliments.
            `,
            "examples": [
                "say 'Here is your compliment!'",
                "say the value of the variable userinput",
                "say the value of the variable toxvar"

            ]
        },
        {
            "title": "Run a Procedure or Program",
            "help": `You must run a program before anything can execute/happen.
            `,
            "examples": [
                "run AskForCompliment"
            ]
        },
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

let handleAnalysisTutorialChange = (newState) => {
    state = newState;
    let examples = document.getElementById('example-analysis-tutorial-actions-list');
    examples.innerHTML = "";
    if (state != null && state in example_analysis_tutorial_commands) {
        let commands = example_analysis_tutorial_commands[state];
        for (var i = 0; i < commands.length; i++) {
            action = commands[i];
            let node = document.createElement('div');
            node.className = "example-analysis-tutorial-action"
            node.innerHTML = `<div class="action-title"><b>${action.title}</b>   <button class="button-help" id="button-help-` + i + `">Help</button></div>`;
            // action.examples.forEach(ex => {
            //     node.innerHTML += `<div class="action-example"><em>${ex}</em></div>`;
            // })
            examples.appendChild(node);
        }
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
        speak: speak
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

let addExampleAnalysisTutorialActions = () => {
    document.getElementById('example-analysis-tutorial-actions').innerHTML = `
        <div id="example-analysis-tutorial-actions-heading">
            <div><b>Anaylsis Tutorial: Here are your commands</b></div>
            <div id="example-analysis-tutorial-actions-direction">&#9660</div>
        </div>
        <div id="example-analysis-tutorial-actions-list"></div>`;
    document.getElementById('example-analysis-tutorial-actions-heading').onclick = () => {
        let actionsList = document.getElementById('example-analysis-tutorial-actions-list');
        let displ = actionsList.style.display === 'block' ? 'none' : 'block';
        document.getElementById('example-analysis-tutorial-actions-direction').innerHTML = displ === 'none' ? "&#9660" : "&#9650";
        actionsList.style.display = displ;
    }

    handleAnalysisTutorialChange("home");
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

let populateModalInitial = () => { 
    document.getElementById("modal-content-paragraph").innerHTML = `
    <ol>
        <li>When you think of the phrase ‘artificial intelligence’ or ‘ai,’ what do you think of? 
            <ul>
                <li><i>Making decisions</i></li>
                <li><i>Learning from patterns</i></li>
                <li><i>Alexa, Google Home, Siri</i></li>
                <li><i>Smart computers</i></li>
            </ul>
        </li>
        <li>When it comes to learning about AI, here are some big AI concepts that you will want to keep in mind. 
            <ol>
                <li><b>Computers perceive the world using sensors.</b> Computers need to take input from you, your friend, or the environment to know what’s going on.</li>
                <li><b>Agents maintain models of the world using representations.</b> It is important to realize that any ‘smart computer’ you know of uses representations or models to depict their own world. </li>
                <li><b>Computers can learn from data.</b> Computers make a decision or know things because they can process a TON of data and learn from patterns in the data.</li>
                <li><b>Making agents interact comfortably with users.</b> It is crucial that any AI agent that interacts with you knows what you want and makes you feel comfortable.</li>
                <li><b>Ethics of AI.</b> Whatever happens with AI, we want to make sure that it is making a good impact on the community. AI can impact society in negative and positive ways, so thinking about the impacts of an application is crucial.</li>
            </ol>
            We will be focusing on <b>maintaining models using representations, computers learning from data to create machine models</b> to learn from data to represent how toxic a statement can be.
            Then, we will be <b>evaluating the ethics of the ML model usage</b> along the way in the tutorial sidebar.

        </li>
    </ol>
    <div class="modal-content-button">
        <button id="modal-next">Next</button>
    </div>
`
}

let populateModalNext = () => { 
    document.getElementById("modal-content-paragraph").innerHTML = `
    In this tutorial, you will be learning that using an API, a machine learning model takes in a sentence you write and outputs how “toxic” the sentence is on a scale of 0 to 1.
    We are aiming to have the user type in a sentence with a low toxicity rate to be nice to each other! 
        <ol>
            <li>First, we will be using an API. <b>What is an API?</b><br>
            API (application program interface) is a set of components with routines, protocols, and tools
            that allows the user to build software! We will be making requests to <b>Google's Toxicity API</b>, 
            and that will allow us to evaluate how "toxic" a phrase is on a scale from 0 to 1. 
            <a href="https://www.perspectiveapi.com/#/home">More info here</a>
                
            </li>
            <li><b>What is machine learning?</b><br>
            Machine learning is when you give lots of data to a computer program and choose a model to “fit” the data, 
            which allows the computer to come up with predictions. The computer uses algorithms to learn patterns, which can range from 
            a simple equation (like the equation of a line) to a very complex system of logic/math results in the best prediction.
            <br><br>
            In this tutorial, Google's Perspective API uses machine learning by analyzing a ton of sentences and learning how "toxic" those sentences are.
            Then, when a user sends a request to request a toxicity score for a random phrase, the Perspective machine learning model
            will be able to return how toxic the phrase is.
            <br><br>
            Read more about an simple definition of machine learning <a href="https://thenextweb.com/neural/2020/04/25/machine-learning-models-explained-to-a-five-year-old-syndication/">here</a>
            </li>
        </ol>
    To begin, we’ll guide you through the tutorial to write your own Convo code!
    <div class="modal-content-button">
        <button id="modal-close">Close</button>
    </div>
    `
    
}

let populateAndDisplayModal = () => {
    populateModalInitial();
    var modal = document.getElementById("myModal");

    // Get the <span> element that closes the modal
    var span = document.getElementsByClassName("close")[0];

    // Open the modal 
    modal.style.display = "block";

    // When the user clicks on <span> (x), close the modal
    span.onclick = function() {
    modal.style.display = "none";
    }

    var nextButton = document.getElementById("modal-next");
    nextButton.onclick = function() {
        populateModalNext();
        var closeButton = document.getElementById("modal-close");
        closeButton.onclick = function() {
            modal.style.display = "none";
        }
    }

    // When the user clicks anywhere outside of the modal, close it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }   
}

let populateHelpModal = () => {
    var allHelpButtons = document.getElementsByClassName("button-help");
    for(var i=0; i<allHelpButtons.length; i++) {
        let stepButton = allHelpButtons[i]
        console.log(stepButton.id);
        stepButton.onclick = function() {
            let stepButtonIdArray = stepButton.id.split("-");
            console.log(stepButtonIdArray);
            let buttonId = parseInt(stepButtonIdArray[stepButtonIdArray.length-1]) // get the ID # 
            populateHelpModalWithInfo(buttonId)
        }
    };
}

let populateHelpModalWithInfo = (i) => {
    let commandForStep = example_analysis_tutorial_commands[state][i];
    let commandTitle = commandForStep.title;
    let commandHelp = commandForStep.help;
    let commandExamples = commandForStep.examples;
    var modalContentHelpParagraph = document.getElementById("modal-content-paragraph");
    modalContentHelpParagraph.innerHTML = "";
    modalContentHelpParagraph.innerHTML += "<div><b>"+commandTitle+"</b></div>";
    modalContentHelpParagraph.innerHTML += "<ol>"
    commandExamples.forEach((command) => {
        modalContentHelpParagraph.innerHTML += "<li><i>"+command+"</i></</li>";
    });
    modalContentHelpParagraph.innerHTML += "</ol>"
    modalContentHelpParagraph.innerHTML += "<br><div>"+commandHelp+"</div>";

    modalContentHelpParagraph.innerHTML += `<div class="modal-content-button">
        <button id="modal-close">Close</button>
    </div>
    `
    var modal = document.getElementById("myModal");

    // Open the modal 
    modal.style.display = "block";

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

    let exampleAnalysisTutorial = document.getElementById('example-analysis-tutorial-actions');
    if (exampleAnalysisTutorial != null) {
        addExampleAnalysisTutorialActions();
    }

    populateAndDisplayModal();
    populateHelpModal();
 
    addAudioPlayer();
});
