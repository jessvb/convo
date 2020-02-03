/**
 * This file contains useful functions for the day of the experiment, which can be 
 * accessed in the console.
 */

/**
 * Only use this method if the system is *really* not recognizing someone's voice.
 */
function displayTextbox() {
    var textbox = document.getElementsByClassName('textbox')[0];
    if (textbox) {
        // TODO: @Kevin please send a log to the server with the userid, timestamp, etc. 
        // stating that the user's voice couldn't be recognized, so the textbox was 
        // displayed.
        displayElement(textbox);
    }
}

/**
 * Only use this method if the user *really* cannot finish the stage.
 */
function displayNextBtn() {
    var nextBtn = document.getElementById('button-container');
    if (nextBtn) {
        // TODO: @Kevin please send a log to the server with the userid, timestamp, etc. 
        // stating that the user could not complete a section, so the next button was
        // displayed
        displayElement(nextBtn);
    }
}

/**
 * Helper function to display element.
 * @param {} elem 
 */

function displayElement(elem) {
    elem.style.display = 'flex';
}