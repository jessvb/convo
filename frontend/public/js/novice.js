const practice_instructions = [
    "create a procedure called pet sounds",
    "say hello world",
    "done",
    "run hello world"
];

let instructionStep = 0;
let handleStepUpdate = (data) => {
    let newStep = data['step'];
    console.log(practice_instructions[newStep]);
    instructionStep = newStep;
}

socketApi.on('stepUpdate', handleStepUpdate);

document.addEventListener('DOMContentLoaded', (event) => {
    initial_utter = "Great job! Now let’s create a procedure that can play cat and dog sounds. Look to the sidebar to see what the end result should look like."
    addUtter("agent-utter", initial_utter, false);
    addUtter("agent-utter", "Let’s get started! How would you like to start?", false);
});
