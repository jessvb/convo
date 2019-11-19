STEP = 0
INSTRUCTIONS = [
    "Begin by typing 'Hello' in the text box.", 
    "Then, type 'Start programming'.",
    "Type 'Hello world'.",
    "Type 'That's it'.",
    "Type 'Yes'.",
    "Congratulations, you just made a program with a conversational agent! Feel free to practice more with the system and get comfortable using it before moving onto the next step. Below are some example phrases you can reference."
]

// This function does the following after Enter is pressed:
// - stores and shows textbox input 
// - populates sidebar instructions
// - returns agent output?
function enterText() {
    // Gets textbox input value
    var typedStr = document.getElementById("textbox").value;
    document.getElementById("textbox").value = "";
    // Adds input value to user transcript
    var transcript = document.getElementById("transcript").innerHTML;
    // document.getElementById("transcript").innerHTML = typedStr + "<br>" + transcript;
    // Shows agent response
    agentResponse = "Insert agent response"
    document.getElementById("transcript").innerHTML = '<span class="red">' + agentResponse + "</span>" + "<br>" + "<span class='blue'>" + typedStr  + "</span>" + "<br>" + transcript;

    // Side Bar 
    var instruction = document.getElementById('sidebarinfo').innerHTML;
    switch (STEP) {
        case 0:
            if (typedStr.includes("Hello")) {
                STEP++;
                break;
            }
        case 1:
            if (typedStr.includes("Start programming")) {
                STEP++;
                break;
            }
        case 2:
            if (typedStr.includes("Hello world")) {
                STEP++;
                break;
            }
        case 3:
            if (typedStr.includes("That's it")) {
                STEP++;
                break;
            }
        case 4:
            if (typedStr.includes("Yes")) {
                STEP++;
                document.getElementById("exampleguide").style.display = "";
                break;
            }
    }
    document.getElementById("sidebarinfo").innerHTML = INSTRUCTIONS[STEP];
}

// This function clears the transcript + restarts instructions when Reset is pressed
function reset() {
    document.getElementById("transcript").innerHTML = "";
    document.getElementById("agent").innerHTML = "";
    STEP = 0;
    document.getElementById("sidebarinfo").innerHTML = INSTRUCTIONS[0]
}

function submit() {
    window.location.href = 'PracticeVoiceSystem.html';
}