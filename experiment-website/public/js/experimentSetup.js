// This javascript file contains methods to set up the experiment, and calls
// functions in experimentProcess to begin the experiment

// ------------------------------ //
// --- Variables to be logged --- //
// ------------------------------ //
// increment currentTestNum before every test: see currTest in
// experimentProcess.js if the click starts a test, then put 'start', if it
// ends, put 'end':
let startOrEndEvent;
// if this click was on an incorrect menu item, make this true:
let wrongItemClick;
// increment this on every click:
let clickNumber = 0;

// number of blocks within a menu:
const NUM_BLOCKS = 4;
// number of items within a block:
const NUM_ITEMS = 4;
// number of predicted items:
const NUM_PREDICTED_ITEMS = 3;


// ------------------ //
// --- On Startup --- //
// ------------------ //
document.addEventListener('DOMContentLoaded', function(event) {
  // ------------------------ //
  // --- Experiment Setup --- //
  // ------------------------ //

  // Create menus with NUMBLOCKS subsections each and NUMITEMS items within each
  // subsection
  createMenus(NUM_BLOCKS, NUM_ITEMS);
  updateMenus();

  // The accuracy is randomly chosen on a per-subject basis to be either high or
  // low (between subjects)
  adaptiveAccuracy = getAccuracy();

  // Whether the control or the fading menu tests are first (within subjects) is
  // randomly assigned
  isControlFirst = getOrderOfControl();


  // ----------------------- //
  // --- Event Listeners --- //
  // ----------------------- //

  // Mouse down event listeners within the menu area:
  document.getElementById('menuarea')
      .addEventListener('mousedown', function(evt) {
        // --- MOUSEDOWN: MENU OPENING AND CLOSING -- //

        // initially set the event logging variables to defaults
        startOrEndEvent = null;
        wrongItemClick = false;

        // remove the fading animation from all menuitems before applying any
        // animations
        let arrItems = Array.prototype.slice.call(
            document.getElementsByClassName('menuitem'));
        removeFade(arrItems);

        let targ = evt.target;
        // if this was a menutitle, open the menu
        if (classIncludes('menutitle', targ)) {
          let menudropdown = targ.getElementsByClassName('menudropdown')[0];

          // start the fading process if we're currently in a fading stage (not
          // control)
          if (currTestType == 'fading') {
            // predict items
            let predictedItems = getPredictedItems(
                NUM_PREDICTED_ITEMS, currCorrectItem, adaptiveAccuracy);
            // animate the unpredicted items fading in
            fadeItems(predictedItems);
          }

          // stop showing the other menus
          let menus = document.getElementsByClassName('menutitle');
          for (let i = 0; i < menus.length; i++) {
            let menu = menus.item(i).getElementsByClassName('menudropdown')[0];
            // check if not the same id as the one we clicked on:
            if (menu.parentElement.id != menudropdown.parentElement.id) {
              // hide menu
              menu.setAttribute('class', 'menudropdown');
              // revert the menutitle's colour to normal
              menu.parentElement.setAttribute('class', 'menutitle');
            } else {
              // this is the menu we clicked on
              // Toggle this menu between shown and not shown:
              toggleShowMenu(menudropdown);

              // if this is the correct menu, and it is now open, set
              // startOrEndEvent to 'start'
              if (isVisible(menudropdown) &&
                  menudropdown.parentElement.id ==
                      currCorrectItem.parentElement.parentElement.parentElement
                          .id) {
                startOrEndEvent = 'start';
              }
            }
          }
        } else {
          // the user clicked on something that wasn't a menu, so hide all menus
          hideAllMenus();
        }

        let nextStage = false;
        let nextTest = false;
        // If this is a menuitem...
        if (classIncludes('menuitem', targ)) {
          // if it's the correct menuitem:
          if (targ == currCorrectItem) {
            // increment the currTest value
            currTest++;
            // set this as an end event
            startOrEndEvent = 'end';
            // if we're done all the tests, go to the next stage (note:
            // currTest is 0-indexed)
            if (currTest >= currTotalTests) {
              nextStage = true;
            } else {
              nextTest = true;
            }
          } else {
            // if it's the wrong menuitem
            wrongItemClick = true;
          }
        }

        // userID for this particular experiment (assoc w survey too):
        let userID = localStorage.getItem('userID');

        // --- MOUSEDOWN: LOG INFO TO GOOGLE FORM -- //
        // log only if the current stage contains 'block'
        if (currStage.includes('block')) {
          document.dispatchEvent(new CustomEvent('log', {
            detail: {
              userID: userID,
              event: evt,
              customName: null,  // if customName is set, it overwrites the name
              clickNumber: clickNumber++,
              currentTestNum: currTest,
              startOrEndEvent: startOrEndEvent,
              wrongItemClick: wrongItemClick,
              currTestType: currTestType,
              adaptiveAccuracy: adaptiveAccuracy,
              currStage: currStage,
              currTestNum: currTest,
              currCorrectItem: currCorrectItem.innerHTML
            }
          }));
        }

        // --- Go to next test or go to next stage --- //
        if (nextStage) {
          // close all the menus
          hideAllMenus();
          // hide the experiment
          hideElement('experimentwrap');
          // go to the next stage
          goToNextStage();
        } else if (nextTest) {
          performSingleTest();
        }
      });

  // ------------------------ //
  // --- Experiment Start --- //
  // ------------------------ //

  // Start the experiment -- see experimentProcess.js
  performExperiment(adaptiveAccuracy, isControlFirst);
});


// ---------------------- //
// --- Helper Methods --- //
// ---------------------- //

/**
 * Checks if the target's class includes the given className. Does null checking
 * too.
 */
function classIncludes(className, target) {
  return target != null && target.getAttribute('class') != null &&
      target.getAttribute('class').includes(className);
}

/**
 * Create menus wherever 'menutitle's are placed in the HTML document. Each menu
 * will have numBlocks number of blocks of related items. Each block will
 * contain numItems number of items.
 * @param {Integer} numBlocks
 * @param {Integer} numItems
 */
function createMenus(numBlocks, numItems) {
  // Find menu divs in the html
  let menutitles = document.getElementsByClassName('menutitle');
  // Create menudropdowns for each menutitle
  for (let i = 0; i < menutitles.length; i++) {
    let innerHTMLString = 'Menu' + (i + 1) + '<div class="menudropdown">';
    for (let numBlock = 0; numBlock < numBlocks; numBlock++) {
      // create block
      innerHTMLString += '<div class="menublock">';
      for (let numItem = 0; numItem < numItems; numItem++) {
        // the item in the menu:
        let item = 'item';
        // create menuitem
        innerHTMLString += '<div class="menuitem">' + item + '</div>'
      }
      // end div for menublock
      innerHTMLString += '</div>';
    }
    // end div for menudropdown
    innerHTMLString += '</div>';

    // place the innerHTMLString in the menutitle div:
    menutitles.item(i).innerHTML = innerHTMLString;
  }
}

/**
 * Toggle whether the menu provided is shown or not.
 * @param {HTML element} menudropdown
 */
function toggleShowMenu(menudropdown) {
  // menudropdown.classList.toggle('showmenu');
  let menutitle = menudropdown.parentElement;
  // If the menu is shown, hide it and remove the menutitle another colour
  if (menudropdown.getAttribute('class').includes('showmenu')) {
    menudropdown.setAttribute('class', 'menudropdown');
    menutitle.setAttribute('class', 'menutitle');
  } else {
    // The menu is hidden, so show it, and make menutitle another colour
    menudropdown.setAttribute('class', 'menudropdown showmenu');
    menutitle.setAttribute('class', 'menutitle menuselected');
  }
}

function hideAllMenus() {
  let menus = document.getElementsByClassName('menutitle');
  // remove 'showmenu' class
  for (let i = 0; i < menus.length; i++) {
    let menutitle = menus.item(i);
    let menudropdown = menutitle.getElementsByClassName('menudropdown')[0];
    // set the menudropdown to not visible
    menudropdown.setAttribute('class', 'menudropdown');
    // remove the additional colour on the menutitle
    menutitle.setAttribute('class', 'menutitle');
  }
}

/**
 * Randomly return an accuracy value of 'high' or 'low'. There is a 50%
 * chance of getting 'high'.
 */
function getAccuracy() {
  let acc = 'high';
  if (Math.random() < 0.5) {
    acc = 'low';
  }
  return acc;
}

/**
 * Randomly return true or false for the order of control. There is a 50% chance
 * of randomly getting true.
 */
function getOrderOfControl() {
  let controlFirst = true;
  if (Math.random() < 0.5) {
    controlFirst = false;
  }
  return controlFirst;
}

/**
 * Set the length of the onset time for the fading animation in the ephemeral
 * tests.
 * @param seconds: length of time in seconds for the fading animation
 */
function setLengthOfOnset(seconds) {
  document.documentElement.style.setProperty(
      '--duration-long-onset', seconds + 's');
}