/* ******************************************************* */
/* ****** Functions Specific to the Opening Survey ******* */
/* ******************************************************* */

/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
function submitAndGo() {
  // Get the user id for this computer and person:
  let userID = localStorage.getItem('userID');
  let uid = localStorage.getItem('uid');

  // Check if we're in the control or the gradual survey stage
  if ((currStage == 'block1_survey' && IS_CONTROL_FIRST) ||
      (currStage == 'block2_survey' && !IS_CONTROL_FIRST)) {
    // we're in the control survey, so submit to the basic likert survey form
    let basiclikert1, basiclikert2, basiclikert3, basiclikert4;
    basiclikert1 = getSelectedRadio('basiclikert1');
    basiclikert2 = getSelectedRadio('basiclikert2');
    basiclikert3 = getSelectedRadio('basiclikert3');
    basiclikert4 = getSelectedRadio('basiclikert4');

    // check for any nulls:
    if (userID == null || uid == null || basiclikert1 == null ||
        basiclikert2 == null || basiclikert3 == null || basiclikert4 == null) {
      console.error(
          'There is an unanswered question. Please report this error to the experimenter.');
      console.error(
          'Collected answers:', userID, uid, basiclikert1, basiclikert2,
          basiclikert3, basiclikert4);
    } else {
      // send input
      sendBasicLikertSurvey(
          userID, uid, basiclikert1, basiclikert2, basiclikert3, basiclikert4);
      // hide survey and go to the next stage
      hideElement('basicsurveywrap');
      goToNextStage();
    }

  } else if (
      (currStage == 'block1_survey' && !IS_CONTROL_FIRST) ||
      (currStage == 'block2_survey' && IS_CONTROL_FIRST)) {
    // we're in the fading survey, so submit to the gradual likert survey form
    let graduallikert1, graduallikert2, graduallikert3, graduallikert4;
    // get user input
    graduallikert1 = getSelectedRadio('graduallikert1');
    graduallikert2 = getSelectedRadio('graduallikert2');
    graduallikert3 = getSelectedRadio('graduallikert3');
    graduallikert4 = getSelectedRadio('graduallikert4');

    // check for any nulls:
    if (userID == null || uid == null || graduallikert1 == null ||
        graduallikert2 == null || graduallikert3 == null ||
        graduallikert4 == null) {
      console.error(
          'There is an unanswered question. Please report this error to the experimenter.');
      console.error(
          'Collected answers:', userID, uid, graduallikert1, graduallikert2,
          graduallikert3, graduallikert4);
    } else {
      // send input
      sendGradualLikertSurvey(
          userID, uid, graduallikert1, graduallikert2, graduallikert3,
          graduallikert4);
      // hide survey and go to the next stage
      hideElement('gradualsurveywrap');
      goToNextStage();
    }
  } else {
    console.error(
        'The current stage is unknown. Results were not submitted to Google Forms.');
    let graduallikert1 = getSelectedRadio('graduallikert1');
    let graduallikert2 = getSelectedRadio('graduallikert2');
    let graduallikert3 = getSelectedRadio('graduallikert3');
    let graduallikert4 = getSelectedRadio('graduallikert4');
    let basiclikert1 = getSelectedRadio('basiclikert1');
    let basiclikert2 = getSelectedRadio('basiclikert2');
    let basiclikert3 = getSelectedRadio('basiclikert3');
    let basiclikert4 = getSelectedRadio('basiclikert4');
    console.error(
        userID, uid, basiclikert1, basiclikert2, basiclikert3, basiclikert4,
        graduallikert1, graduallikert2, graduallikert3, graduallikert4);
  }
}

// The following function was created with: curl -sL goo.gl/jUkahv | python2 -
// https://docs.google.com/forms/d/1Yw9xtBUoy5jDYmQlipbLXmy2JC3yW42ND8LyP7dz0H0/edit

// Gradual Likert Survey submission function
// submits to the google form at this URL:
// docs.google.com/forms/d/1Yw9xtBUoy5jDYmQlipbLXmy2JC3yW42ND8LyP7dz0H0/edit#responses
function sendGradualLikertSurvey(
    userid, uid, graduallikert1, graduallikert2, graduallikert3,
    graduallikert4) {
  var formid = 'e/1FAIpQLSc0y2VWxeOt0k3PrN3jxxiSqzmvmMRiTf0unY0yymSfJtGdqg';
  var data = {
    'entry.1764503663': userid,
    'entry.1469494170': uid,
    'entry.1180349519': graduallikert1,
    'entry.1292228520': graduallikert2,
    'entry.2131411416': graduallikert3,
    'entry.1836131283': graduallikert4
  };
  var params = [];
  for (key in data) {
    params.push(key + '=' + encodeURIComponent(data[key]));
  }
  // Submit the form using an image to avoid CORS warnings.
  (new Image).src = 'https://docs.google.com/forms/d/' + formid +
      '/formResponse?' + params.join('&');
}



// The following function was created with: curl -sL goo.gl/jUkahv | python2 -
// https://docs.google.com/forms/d/1j6Ro3hTZaxGaQ1D3oW0hIzLC9bAJh4D1N2NLI5SoxAg/edit

// Basic Likert Survey submission function
// submits to the google form at this URL:
// docs.google.com/forms/d/1j6Ro3hTZaxGaQ1D3oW0hIzLC9bAJh4D1N2NLI5SoxAg/edit
function sendBasicLikertSurvey(
    userid, uid, basiclikert1, basiclikert2, basiclikert3, basiclikert4) {
  var formid = 'e/1FAIpQLSeWnYMiC6XTKDn_KbMmsTnR5JKlF0mO7joYYYrCR2JYAcM1Iw';
  var data = {
    'entry.1764503663': userid,
    'entry.1867549483': uid,
    'entry.1492751820': basiclikert1,
    'entry.248355498': basiclikert2,
    'entry.1345795253': basiclikert3,
    'entry.371927758': basiclikert4
  };
  var params = [];
  for (key in data) {
    params.push(key + '=' + encodeURIComponent(data[key]));
  }
  // Submit the form using an image to avoid CORS warnings.
  (new Image).src = 'https://docs.google.com/forms/d/' + formid +
      '/formResponse?' + params.join('&');
}
