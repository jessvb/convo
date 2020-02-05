socketApi.on('advancedInstructions', (data) => {
    let instructions = document.getElementById('instruction');
    let sounds = data.sounds;
    instructions.innerHTML = `
        <div>Create a program that does the following:</div>
        <ol id="advanced-instruction-list">
            <li>Use a <b>while</b> loop</li>
            <li>Listen to user input <b>${data.iters}</b> times</li>
            <li>
                Every time it listens, if the user input is <b>'${sounds[0]}'</b>, play the <b>${sounds[0]}</b> sound.
                If the  user input is, <b>'${sounds[1]}'</b>, play the <b>${sounds[1]}</b> sound.
            </li>
        <ol>
    `;
});
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
                <div>Something went wrong. Please refresh the page.</div>
            </div>
        </div>`;
    document.getElementById('goal').innerHTML = `
        <div id="goal-heading">
            <div><b>Advanced Stage Goal</b></div>
        </div>
        <div id="goal-container">
            <p>
                Watch this video to see the goal for this portion of the study.
            </p>
            <iframe width="100%"
                    src="https://www.youtube.com/embed/TiCcaTJJP4Y"
                    frameborder="0"
                    allow="accelerometer; encrypted-media; gyroscope; picture-in-picture"
                    allowfullscreen>
            </iframe>
        </div>`;

    initial_utter1 = "Great job in the novice stage! Did you notice that I only listened for user input once after you ran the procedure?"
    initial_utter2 = "This time, let’s add a countdown. I will continue to listen for user input until I’ve responded five times."
    addUtter("agent-utter", initial_utter1, false);
    addUtter("agent-utter", initial_utter2, false);
    addUtter("agent-utter", "Let’s get started! How would you like to start?", false);
});