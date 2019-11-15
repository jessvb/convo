// once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', function(event) {
  let btns = document.getElementsByClassName('next');
  for (let i = 0; i < btns.length; i++) {
    let btn = btns[i];
    btn.addEventListener('click', next);
  }
});

/**
 * Brings up a notification with the given message and button. This is called in
 * experimentProcess.js.
 */
function notify(msg) {
  // update the message in the notification html
  let msgArea = document.getElementById('msgarea');
  msgArea.innerText = msg;
  // show the notificationwrap
  showElement('notificationwrap', 'grid');
}

/**
 * Close the notification and go to the next stage of the experiment.
 */
function next() {
  hideElement('notificationwrap');
  goToNextStage();
}