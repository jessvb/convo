/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
let submitAndGo = () => {
    let sid = localStorage.getItem('sid');
    let age = $('#age').val();
    let sex = $('#sex').val();
    let genderTextBox = $('#gender-textbox').val();
    let firstLanguage = $('#firstLanguage').val();
    let level = $('#level').val();
    let languages = $('#languages-select').val();
    let languagesOther = $('#languages-textbox').val();
    let agents = $('#agents-select').val();
    let agentsOther = $('#agents-textbox').val();

    if (sid == null || age == null || firstLanguage == null || level == null || sex == null || languages == null || agents == null ) {
        alert('There is an unanswered question. Please report this error to the experimenter.');
        alert(`Collected answers: ${sid}; ${age}; ${sex}; ${genderTextBox}; ${firstLanguage}; ${level}; ${languages}; ${languagesOther}; ${agents}; ${agentsOther}`);
    } else {
        // set advanced / not advanced in local storage for stages-process.js:
        localStorage.setItem('isAdvanced', JSON.stringify({ value: level == 'advanced' }));

        // if selected "other", add the "other" language
        if (languages.includes('other') && languagesOther)
            languages.push(languagesOther);

        // if selected "other", add the "other" agent
        if (agents.includes('other') && agentsOther)
            agents.push(agentsOther);

        // if prefer to self-describe, use text box answer
        if (sex === 'other' && genderTextBox)
            sex = genderTextBox;

        surveyData = {
            "age": age,
            "gender": sex,
            "first_language": firstLanguage,
            "level": level,
            "programming_languages": languages,
            "conv_agents": agents
        }

        socketApi.emit("survey", {
            "sid": sid,
            "type": "demographics",
            "data": surveyData
        });

        window.location.href = '/practice-info';
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
            if (pairedQuesElm)
                pairedQuesElm.style.display = 'block';
        } else if (opt.value === "other" && !opt.selected) {
            ansElm.style.display = 'none';
            // if there's a paired question element, then hide it too:
            if (pairedQuesElm)
                pairedQuesElm.style.display = 'none';
        }
    }
};
