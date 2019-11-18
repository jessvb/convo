STEP = 0
INSTRUCTIONS = [
    "Begin by typing 'Hello' in the text box.", 
    "Then, type 'Start programming'.",
    "Type 'Hello world'.",
    "Type 'That's it'.",
    "Type 'Yes'.",
    "Congratulations, you just made a program with a conversational agent! Feel free to practice more with the system and get comfortable using it before moving onto the next step."
]

// This function stores and shows textbox input after Enter is pressed
// and populates sidebar instructions
function enterText() {
    var typedStr = document.getElementById("textbox").value;
    document.getElementById("textbox").value = "";
    var transcript = document.getElementById("transcript").innerHTML;
    document.getElementById("transcript").innerHTML = typedStr + "<br>" + transcript;

    var instruction = document.getElementById('sidebarinfo').innerHTML;
    // check if typed str matches instruction
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
                break;
            }
    }
    document.getElementById("sidebarinfo").innerHTML = INSTRUCTIONS[STEP];
}

// This function clears the transcript + restarts instructions when Reset is pressed
function reset() {
    document.getElementById("transcript").innerHTML = "";
    STEP = 0;
    document.getElementById("sidebarinfo").innerHTML = INSTRUCTIONS[0]
}

function getInstruction() {
    
}