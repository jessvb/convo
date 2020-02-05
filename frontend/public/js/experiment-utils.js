/**
 * This file contains useful functions for the day of the experiment, which can be
 * accessed in the console.
 */

/**
 * Only use this method if the system is *really* not recognizing someone's voice.
 */
let displayTextbox = () => {
    var textbox = document.getElementsByClassName('textbox')[0];
    if (textbox) {
        let data = {
            'sid': getUniqueId(),
            'currPart': localStorage.getItem('currPart'),
            'currStage': localStorage.getItem('currStage')
        }
        socketApi.emit('displayTextbox', data);
        displayElement(textbox);
    }
}

/**
 * Only use this method if the user *really* cannot finish the stage.
 */
let displayNextBtn = () => {
    var nextBtn = document.getElementById('button-container');
    if (nextBtn) {
        let data = {
            'sid': getUniqueId(),
            'currPart': localStorage.getItem('currPart'),
            'currStage': localStorage.getItem('currStage')
        }
        socketApi.emit('displayButton', data);
        displayElement(nextBtn);
    }
}

/**
 * Helper function to display element.
 * @param {} elem
 */
let displayElement = (elem) => {
    elem.style.display = 'flex';
}
