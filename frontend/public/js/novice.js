const stage_instructions = [
    "Create a procedure called pet sounds",
    "Get user input",
    "animal",
    "If animal is dog play the bark sound",
    "Done",
    "No",
    "If animal is cat, play the meow sound",
    "Done",
    "No",
    "Done",
    "Run pet sounds"
];

let instructionStep = 0;
let handleStepUpdate = (data) => {
    instructionStep = data['step'];
    document.getElementById('instruction').innerHTML = `<em>"${stage_instructions[instructionStep]}"</em>`;
}

socketApi.on('stepUpdate', handleStepUpdate);
socketApi.on('stageCompleted', () => {
    document.getElementById('instruction-container').innerHTML = `
        <div class="stage-completed">
            Stage completed! <b>Please click the button to move on to the next stage.</b>
        </div>`;
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('instructions').innerHTML = `
        <div id="instructions-heading">
            <div><b>Instructions</b></div>
        </div>
        <div id="instruction-container">
            <div id="instruction-say"><b>Say</b></div>
            <div id="instruction"></div>
        </div>`;
    handleStepUpdate({ "step": 0 });

    initial_utter = "Great job! Now let’s create a procedure that can play cat and dog sounds. Look to the sidebar to see what the end result should look like."
    addUtter("agent-utter", initial_utter, false);
    addUtter("agent-utter", "Let’s get started! How would you like to start?", false);
});
