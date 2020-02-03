socketApi.on('stageCompleted', () => {
    document.getElementById('instruction-container').innerHTML = `
        <div class="stage-completed">
            Stage completed! <b>Please click the button to move on to the next stage.</b>
        </div>`;
    document.getElementById('button-container').style.display = 'flex';
});

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('instructions').innerHTML = `
        <div id="instructions-heading">
            <div><b>Instructions</b></div>
        </div>
        <div id="instruction-container">
            <div id="instruction">
                <div>Create a program that does the following:</div>
                <ol>
                    <li>Use a <b>while</b> loop</li>
                    <li>Listen to user input <b>five</b> times</li>
                    <li>Play corresponding sound <b>five</b> times</li>
                <ol>
            </div>
        </div>`;

    initial_utter1 = "Great job in the novice stage! Did you notice that I only listened for user input once after you ran the procedure?"
    initial_utter2 = "This time, let’s add a countdown. I will continue to listen for user input until I’ve responded five times."
    addUtter("agent-utter", initial_utter1, false);
    addUtter("agent-utter", initial_utter2, false);
    addUtter("agent-utter", initial_utter3, false);
    addUtter("agent-utter", "Let’s get started! How would you like to start?", false);
});
