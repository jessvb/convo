const practice_instructions = [
    "Create a procedure called hello world",
    "Say hello world",
    "Done",
    "Run hello world"
];

let instructionStep = 0;
let handleStepUpdate = (data) => {
    console.log('')
    instructionStep = data['step'];
    document.getElementById('instruction').innerHTML = `Say <em>"${practice_instructions[instructionStep]}"</em>`
}

socketApi.on('stepUpdate', handleStepUpdate);
socketApi.on('stageCompleted', () => {
    console.log("Stage Completed!");
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('instructions').innerHTML = `
        <div id="instructions-heading">
            <div><b>Instructions</b></div>
        </div>
        <div id="instruction"></div>`;
    handleStepUpdate({ "step": 0 });

    initial_utter = "Hello! Let’s create a procedure that says “Hello world!” today. If you ever need help, just say “I need help.”"
    addUtter("agent-utter", initial_utter, false);
    addUtter("agent-utter", "How would you like to start?", false);
});
