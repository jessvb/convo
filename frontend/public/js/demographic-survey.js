/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
let submitAndGo = () => {
    // Get the user id for this computer and person:
    let userID = localStorage.getItem('userID');
    let uid = localStorage.getItem('uid');

    let age = document.getElementById('age').value;
    let sex = document.getElementById('sex').value;
    let genderTextBox = document.getElementById('gender-textbox').value;
    let firstLanguage = document.getElementById('firstLanguage').value;
    let level = document.getElementById('level').value;
    let programmingLanguages = document.getElementById('languages-select').value;
    let programmingLanguagesTextBox = document.getElementById('languages-textbox').value;
    let convAgents = document.getElementById('agents-select').value;
    let convAgentsTextBox = document.getElementById('agents-textbox').value;


    if (userID == null || uid == null || age == null || sex == null ||
        firstLanguage == null || level == null ||
        programmingLanguages == null || convAgents == null) {
        window.alert('There is an unanswered question. Please report this error to the experimenter.');
        window.alert('Collected answers: ', userID, age, sex, genderTextBox, firstLanguage, level, programmingLanguages, programmingLanguagesTextBox, convAgents, convAgentsTextBox);
    } else {
        // set advanced / not advanced in local storage for stages-process.js:
        if (level == 'advanced'){
            localStorage.setItem('isAdvanced', JSON.stringify({
                value: true
            }));
        } else {
            localStorage.setItem('isAdvanced', JSON.stringify({
                value: false
            }));
        }
        let url = 'practice-info';
        window.open(url, '_self');
    }
};

// The following function was made with: curl -sL goo.gl/jUkahv | python2 -
// https://docs.google.com/forms/d/1cjwOdJUqsqpqsWqllwyK2MYCzhkp5lb_ElrvrltfuLM/edit

// Opening Survey submission function
// submits to the google form at this URL:
// docs.google.com/forms/d/1cjwOdJUqsqpqsWqllwyK2MYCzhkp5lb_ElrvrltfuLM/edit
let sendDemographicSurvey = (userid, uid, age, sex, computerusage, pointingdevice) => {
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
    (new Image).src = `https://docs.google.com/forms/d/${formid}/formResponse?${params.join("&")}`;
};

// This function creates an Other text box if Other is clicked in a "Select Multiple" question
let showOtherTextBox = (sel, id) => {
    var opt;
    var len = sel.options.length;
    for (var i = 0; i < len; i++) {
        opt = sel.options[i];

        var ansElm = document.getElementById(id);
        // get any paired question elements, if there is one
        var pairedQuesElm;
        if (ansElm.classList.contains('paired')) {
            var siblingElms = ansElm.parentElement.childNodes;
            for (let j = 0; j < siblingElms.length; j++) {
                if (siblingElms[j].classList && siblingElms[j].classList.contains('question') && siblingElms[j].classList.contains('paired')) {
                    pairedQuesElm = siblingElms[j];
                    break;
                }
            }
        }

        if (opt.value === "other" && opt.selected) {
            ansElm.style.display = 'block';
            // if there's a paired question element, then display it too:
            if (pairedQuesElm) {
                pairedQuesElm.style.display = 'block';
            }
        } else if (opt.value === "other" && !opt.selected) {
            ansElm.style.display = 'none';
            // if there's a paired question element, then hide it too:
            if (pairedQuesElm) {
                pairedQuesElm.style.display = 'none';
            }
        }
    }
};