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

  let age, sex, computerUsage, email;
  // get user input
  age = document.getElementById('age').value;
  sex = document.getElementById('sex').value;
  computerUsage = document.getElementById('compUsage').value;
  pointingDevice = document.getElementById('pointingDevice').value;
  if (
    userID == null || uid == null || age == null || sex == null ||
    computerUsage == null || pointingDevice == null) {
    console.error(
      'There is an unanswered question. Please report this error to the experimenter.');
    console.error('Collected answers:', userID, age, sex, computerUsage, pointingDevice);
  } else {
    // send input
    sendOpeningSurvey(userID, uid, age, sex, computerUsage, pointingDevice);

    // go to next page (experiment page)
    window.location.href = 'gradualOnsetExperiment.html';
  }
}

// The following function was made with: curl -sL goo.gl/jUkahv | python2 -
// https://docs.google.com/forms/d/1cjwOdJUqsqpqsWqllwyK2MYCzhkp5lb_ElrvrltfuLM/edit

// Opening Survey submission function
// submits to the google form at this URL:
// docs.google.com/forms/d/1cjwOdJUqsqpqsWqllwyK2MYCzhkp5lb_ElrvrltfuLM/edit
function sendOpeningSurvey(
  userid,
  uid,
  age,
  sex,
  computerusage,
  pointingdevice) {
  var formid = "e/1FAIpQLScd3bGWrwzLRGFvO2Vn8czBQcCdYkZd5EUt1hccNeiAd_aoiA";
  var data = {
    "entry.232033829": userid,
    "entry.1656626167": uid,
    "entry.1787724413": age,
    "entry.1665193410": sex,
    "entry.1102087624": computerusage,
    "entry.769108803": pointingdevice
  };
  var params = [];
  for (key in data) {
    params.push(key + "=" + encodeURIComponent(data[key]));
  }
  // Submit the form using an image to avoid CORS warnings.
  (new Image).src = "https://docs.google.com/forms/d/" + formid +
    "/formResponse?" + params.join("&");
}

// This function creates an Other text box if Other is clicked in a "Select Multiple" question
function showOtherTextBox(sel, id) {
    var opts = [], opt;
    var len = sel.options.length;
    for (var i = 0; i < len; i++) {
      opt = sel.options[i];

      if (opt.value === "other" && opt.selected) {
        opts.push(opt);
        // alert(opt.value);
        document.getElementById(id).style.display = 'block';
      }
      else {
        document.getElementById(id).style.display = 'none'; 
      }
    }
}