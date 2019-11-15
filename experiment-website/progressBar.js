// This file contains methods to update the progress bar

// total "length" value for calculating progress
const totalLengthVal = getTotalLengthVal();
localStorage.setItem('totalLengthVal', totalLengthVal);


/**
 * This updates the progress bar, providing feedback for the user.
 */
function updateProgressBar() {
  // Percent complete: currPos/totalLengthVal
  // total "length" of experiment: totalLengthVal (global constant)
  // current "position" in the experiment: getCurrPosVal()
  let currPos = getCurrPosVal();
  let percentComplete = currPos / totalLengthVal;
  document.getElementsByClassName('progressBar')[0].innerText =
      'Progress: ' + Math.floor(percentComplete * 100) + '%';
}

function getTotalLengthVal() {
  // total value includes end survey too, with a value of surveyValue
  return parseInt(localStorage.getItem('surveyVal')) +
      getCurrPosVal(STAGES.length);
}

/**
 * Gets the current position value for the progress bar. If stage isn't set, it
 * defaults to the current stage (global var).
 * @param {Integer} stage: the stage you're getting the value for
 */
function getCurrPosVal(stage) {
  if (stage == null) {
    stage = stageIndex;
  }

  let numSurveysComplete = 1;  // already completed the first survey
  let numPracticesComplete = 0;
  let numHalfBlocksComplete = 0;

  // loop through the stages (not including the current stage) and add stuff up:
  for (let i = 0; i < stage; i++) {
    if (STAGES[i].includes('practice') && !STAGES[i].includes('notify')) {
      numPracticesComplete++;
    } else if (STAGES[i].includes('block') && STAGES[i].includes('half')) {
      numHalfBlocksComplete++;
    } else if (STAGES[i].includes('survey')) {
      numSurveysComplete++;
    }
  }

  // each survey counts for surveyValue points
  // each test counts for 1 value point
  // each completed practice counts for NUM_PRACTICE_TESTS
  // each completed half block counts for NUM_TESTS_PER_BLOCK / 2
  return numSurveysComplete * parseInt(localStorage.getItem('surveyVal')) +
      currTest * 1 + numPracticesComplete * NUM_PRACTICE_TESTS +
      numHalfBlocksComplete * NUM_TESTS_PER_BLOCK / 2;
}