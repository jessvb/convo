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
            <div id="instruction">Create a program that does this.</div>
        </div>`;

    initial_utter1 = "Great job! Did you notice that I only listened for user input once after you ran the procedure?"
    initial_utter2 = "This time, let’s add a countdown. I will continue to listen for user input until I’ve responded five times."
    initial_utter3 = "Here is what the end result looks like."
    addUtter("agent-utter", initial_utter1, false);
    addUtter("agent-utter", initial_utter2, false);
    addUtter("agent-utter", initial_utter3, false);
    addUtter("agent-utter", "Let’s get started! How would you like to start?", false);
});
