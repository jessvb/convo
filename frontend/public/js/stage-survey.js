// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => createDOM());

/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
let submitAndGo = () => {
    // Get the user id for this computer and person:
    let sid = localStorage.getItem('sid');

    // get the number of shortAns and likert q's:
    let numLikertQs = localStorage.getItem('numLikertQs');
    let numShortAnsQs = localStorage.getItem('numShortAnsQs');

    let likertAns = [];
    for (let i = 0; i < numLikertQs; i++) {
        let radios = document.getElementsByName(`l${i}`);
        radios.forEach(radio => {
            if (radio.checked) {
                likertAns.push(radio.value);
            }
        });
    }
    let shortAns = [];
    for (i = 0; i < numShortAnsQs; i++) {
        shortAns.push(document.getElementById(`s${i}`).value);
    }

    // Send and go to next stage
    if (sid == null || likertAns.length < numLikertQs || shortAns.length < numShortAnsQs) {
        alert('There is an unanswered question. Please report this error to the experimenter.');
        alert(`Collected answers: ${sid}; ${currStage}; ${currPart}; ${likertAns}; ${shortAns}`);
    } else {
        localStorage.setItem('doneSurvey', JSON.stringify({ value: true }));
        let currStage = localStorage.getItem('currStage');
        let completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
        let currPart = completedParts[completedParts.length - 1];
        let isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;

        // TODO: store survey data!!!
        // --> Make sure it's stored wrt currStage (novice/adv)
        // --> Make sure it's stored wrt currPart (v,t,v+t)
        window.alert('Survey data is not being stored. TODO: @Kevin store data in server.');
        window.alert('Collected answers: ' + sid + '; ' + currStage + '; ' + currPart + '; ' +
            likertAns + '; ' + shortAns);

        // getNextStageUrl is found in stages-process.js
        // window.location.href = getNextStageUrl(currStage, completedParts, true, isAdvanced);
    }
};

let capitalize = (s) => {
    return s.charAt(0).toUpperCase() + s.substr(1).toLowerCase();
}

/**
 * Programatically create the survey using the currStage (novice, advanced, finalSurvey)
 * and completedParts information found in localstorage.
 */
let createDOM = () => {
    // Create the survey
    let currStage = localStorage.getItem('currStage');
    let completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
    let currPart = completedParts[completedParts.length - 1];

    let system = '';
    let verbage = '';
    let finalSurvey = false;
    if (currStage != 'finalSurvey') {
        if (currPart.includes('voice') && currPart.includes('text')) {
            system = 'voice/text';
            verbage = 'speaking and/or typing';
        } else if (currPart.includes('voice')) {
            system = 'voice';
            verbage = 'speaking-only';
        } else if (currPart.includes('text')) {
            system = 'text';
            verbage = 'typing-only';
        }
    } else {
        finalSurvey = true;
    }

    // #1: Add heading for the likert scale questions
    let info = document.getElementById('info');
    if (!finalSurvey) {
        info.innerHTML = `
            <h2>${capitalize(system)}-based System Survey</h2>
            <h3>${capitalize(currStage)} Stage</h3>
            <p>
                How strongly do you agree with the following statements with regards to your
                experience with the <strong>${system}-based</strong> system (i.e., the ${verbage} system)?
            </p>`
    } else {
        // Final survey
        info.innerHTML = `
            <h2>System Comparison - Final Survey</h2>
            <p>How strongly do you prefer each system compared to the others?</p>`;
    }

    info.innerHTML += '<div id="likert-wrap"><form id="likert-form"></form></div>';
    let form = document.getElementById('likert-form');

    // #2: Add the likert scale questions
    // E.g.,
    // <label class="statement">
    //     I found it difficult to complete the goal with the voice-based system.
    // </label>
    // <ul class='likert answer' id="l1">
    //     <li>
    //         <input type="radio" name="l1" value="strong_agree">
    //         <label>Strongly agree</label>
    //     </li>
    //     <li>
    //         <input type="radio" name="l1" value="agree">
    //         <label>Agree</label>
    //     </li>
    //     <li>
    //         <input type="radio" name="l1" value="neutral">
    //         <label>Neutral</label>
    //     </li>
    //     <li>
    //         <input type="radio" name="l1" value="disagree">
    //         <label>Disagree</label>
    //     </li>
    //     <li>
    //         <input type="radio" name="l1" value="strong_agree">
    //         <label>Strongly disagree</label>
    //     </li>
    // </ul>
    let likertQs = [];
    let labels = [];
    let values = [];

    if (!finalSurvey) {
        likertQs = [
            `I found it difficult to complete the goal with the ${system}-based system.`,
            `I found programming with the ${system}-based system difficult to use.`,
            `I am satisfied programming with the ${system}-based system.`,
            `I found programming with the ${system}-based system efficient to use.`
        ];

        // all the same labels/values for each question, in this case:
        likertQs.forEach(() => {
            labels.push(['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']);
            values.push(['strongly_agree', 'agree', 'neutral', 'disagree', 'strongly_disagree']);
        });

        // programmatically create the likert scale questions
        addLikertQsToDOM(form, likertQs, values, labels);
    } else {
        // I preferred: text ←------→ voice (5-point slider)
        // I preferred: voice ←------→ voice+text (5-point slider)
        // I preferred: voice+text ←------→ text (5-point slider)
        labels = [
            ['Text-based system strongly', 'Text-based system', 'Either system', 'Voice-based system', 'Voice-based system strongly'],
            ['Voice-based system strongly', 'Voice-based system', 'Either system', 'Voice/text-based system', 'Voice/text-based system strongly'],
            ['Voice/text-based system strongly', 'Voice/text-based system', 'Either system', 'Text-based system', 'Text-based system strongly']
        ];

        values = [
            ['strongly_text', 'text', 'either', 'voice', 'strongly_voice'],
            ['strongly_voice', 'voice', 'either', 'voice-text', 'strongly_voice-text'],
            ['strongly_voice-text', 'voice-text', 'either', 'text', 'strongly_text']
        ];

        // all the same questions in this case:
        labels.forEach(() => { likertQs.push('I preferred:') });

        // programmatically create the likert scale preference questions
        let domInd = addLikertQsToDOM(form, likertQs, values, labels);

        // put a paragraph to split up the questions:
        form.innerHTML += '<p>How strongly do you agree with the following statements?</p>';

        let additionalLikertQs = [
            'I think programming with just voice is easier than programming with just text.',
            'I think programming with just text is easier than programming with just both voice and text.',
            'I think programming with just voice is easier than programming with both voice and text.',
            'I think programming with just text is frustrating or hard.',
            'I think programming with just voice is frustrating or hard.',
            'I think programming with both voice and text is frustrating or hard.',
            'I enjoyed the process of trying to complete the tasks.',
            'I think being able to program using voice is useful.',
            'I like being able to program using voice.',
            'If I could, I would continue to learn how to program using voice.',
            'I am a programmer.'
        ];

        let additionalLabels = [];
        let additionalValues = [];
        additionalLikertQs.forEach((question) => {
            additionalLabels.push(['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']);
            additionalValues.push(['strongly_agree', 'agree', 'neutral', 'disagree', 'strongly_disagree']);
            // Even though all the likert q's will be added to the DOM via the 'additional...' variables,
            // we still need to make sure the variable likertQs has *all* likert questions s.t. we know
            // the total number of q's (for checking if users have completed every question):
            likertQs.push(question);
            labels.push(['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']);
            values.push(['strongly_agree', 'agree', 'neutral', 'disagree', 'strongly_disagree']);
        });

        // programmatically create the additional likert scale questions
        addLikertQsToDOM(form, additionalLikertQs, additionalValues, additionalLabels, domInd);
    }

    // store the total number of likertQ's s.t. we can check if all are completed later:
    localStorage.setItem('numLikertQs', likertQs.length);

    // #3: Add headings for the short answer questions
    // <h2>Voice-based System Survey</h2>
    // <h3>Novice Stage</h3>
    // <p>
    //     Answer the following questions with regards to your experience with the
    //     <strong>voice-based</strong> system (i.e., the speaking-only system).
    // </p>
    if (!finalSurvey) {
        form.innerHTML += `
            <h2>${capitalize(system)}-based System Survey</h2>
            <h3>${capitalize(currStage)} Stage</h3>
            <p>
                Answer the following questions with regards to your
                experience with the <strong>${system}-based</strong> system (i.e., the ${verbage} system).
            </p>`;
        // form.innerHTML += '<h2>' + (system.charAt(0).toUpperCase() + system.substring(1)) +
        //     '-based System Survey</h2>' + '<h3>' + (currStage.charAt(0).toUpperCase() +
        //         currStage.substring(1)) + ' Stage</h3>' + '<p>Answer the following questions ' +
        //     'with regards to your experience with the <strong>' + system +
        //     '-based</strong> system (i.e., the ' + verbage + ' system)?' + '</p>';
    } else {
        // final survey
        form.innerHTML += `
            <h2>System Comparison - Final Survey</h2>
            <p>Answer the following questions with regards to your experience.</p>`;
    }

    // #4: Add the short answer questions
    // E.g.,
    // <label class="statement">
    //     What did you like about programming with the voice-based system?
    // </label>
    // <textarea class="answer" id="s1" type="text" placeholder="I liked..."></textarea>
    let shortAnsQs = [];
    let placeholders = [];
    if (!finalSurvey) {
        shortAnsQs = [
            `What did you like about programming with the ${system}-based system?`,
            `What was frustrating about programming with the ${system}-based system? How could we make it less frustrating?`,
            'What did you wish you could say to the agent? What didn’t the agent understand?',
            'What features can we add, change, or remove to make the system better?'
        ];
        placeholders = [
            'I liked...',
            'You could improve the system by...',
            'I wish I could have said things like...',
            'You could add...'
        ];
    } else {
        // final survey
        shortAnsQs = [
            'We want the agent to eventually be able to explain things about how it works. '
                + 'If you were to ask the agent any question, what would you ask it? '
                + 'Please list as many questions as you can think of.',
            'What challenges did you run into while interacting with the agent?',
            'What questions do you have about the system?'
        ];
        placeholders = [
            'I would ask the system...',
            'Some things I found challenging were...',
            'I was wondering...'
        ];
    }

    // store the total number of shortAnsQ's s.t. we can check if all are completed later:
    localStorage.setItem('numShortAnsQs', shortAnsQs.length);

    for (let i = 0; i < shortAnsQs.length; i++) {
        console.log(`Adding short answer questions: ${shortAnsQs[i]}`);
        form.innerHTML += `
            <label class="statement">${shortAnsQs[i]}</label>
            <textarea class="answer" id="s${i}" type="text" placeholder="${placeholders[i]}"></textarea>`;
    }

    // #5: add the 'next' button
    // <div id="button-container">
    //     <button type="button" class="btn btn-primary submit" id="btn-next">
    //         Next
    //     </button>
    // </div>
    console.log('Adding button.')
    form.innerHTML += `
        <div id="button-container">
            <button type="button" class="btn btn-primary submit" id="btn-next">Next</button>
        </div>`;
};

/**
 * Adds likert scale questions to the DOM.
 * @param {*} form
 * @param {*} likertQs
 * @param {*} values
 * @param {*} labels
 * @param {*} prevIndex : If other likert q's have been added to the DOM, we want to make sure
 * the ID of the DOM elements aren't overwritten, so enter the value that was returned by the
 * last call to addLikertQsToDOM() for prevIndex.
 */
function addLikertQsToDOM(form, likertQs, values, labels, prevIndex) {
    // per question ~ i
    // per radio button ~ j
    if (!prevIndex) {
        prevIndex = 0;
    }
    let i;
    for (i = 0; i < likertQs.length; i++) {
        form.innerHTML += `<label class="statement">${likertQs[i]}</label>`;
        form.innerHTML += `<ul class="likert answer" id="l${(i + prevIndex)}"></ul>`;
        let ul = document.getElementById(`l${i + prevIndex}`);

        for (let j = 0; j < labels[i].length; j++) {
            let li = document.createElement("li");
            let input = document.createElement("input");
            input.type = "radio";
            input.name = `l${i + prevIndex}`;
            input.value = values[i][j];
            let label = document.createElement("label");
            label.innerHTML = labels[i][j];
            li.appendChild(input);
            li.appendChild(label);
            ul.appendChild(li);
        }
    }

    return i + prevIndex;
}
