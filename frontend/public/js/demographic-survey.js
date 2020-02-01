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
        window.alert('Collected answers: ' + userID + '; ' + age + '; ' + sex + '; ' + genderTextBox +
            '; ' + firstLanguage + '; ' + level + '; ' + programmingLanguages + '; ' +
            programmingLanguagesTextBox + '; ' + convAgents + '; ' + convAgentsTextBox);
    } else {
        // set advanced / not advanced in local storage for stages-process.js:
        if (level == 'advanced') {
            localStorage.setItem('isAdvanced', JSON.stringify({
                value: true
            }));
        } else {
            localStorage.setItem('isAdvanced', JSON.stringify({
                value: false
            }));
        }

        // todo del:
        window.alert('Survey data is not being stored. TODO: @Kevin store data in server.');

        let url = 'practice-info';
        window.open(url, '_self');
    }
};

// This function creates an Other text box if Other is clicked in a "Select Multiple" question
let showOtherTextBox = (sel, id) => {
    let opt;
    let len = sel.options.length;
    for (let i = 0; i < len; i++) {
        opt = sel.options[i];

        let ansElm = document.getElementById(id);
        // get any paired question elements, if there is one
        let pairedQuesElm;
        if (ansElm.classList.contains('paired')) {
            let siblingElms = ansElm.parentElement.childNodes;
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
