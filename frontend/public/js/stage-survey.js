// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    createDOM();
});

/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
var submitAndGo = () => {
    // Get the user id for this computer and person:
    var sid = localStorage.getItem('sid');

    // get the number of shortAns and likert q's:
    var numLikertQs = localStorage.getItem('numLikertQs');
    var numShortAnsQs = localStorage.getItem('numShortAnsQs');

    var likertAns = [];
    for (var i = 0; i < numLikertQs; i++) {
        var radios = document.getElementsByName('l' + i);
        radios.forEach(radio => {
            if (radio.checked) {
                likertAns.push(radio.value);
            }
        });
    }
    var shortAns = [];
    for (i = 0; i < numShortAnsQs; i++) {
        shortAns.push(document.getElementById('s' + i).value);
    }


    // TODO test & delete:
    console.log('short ans: ', shortAns);
    console.log('likert ans: ', likertAns);
    if (sid == null || likertAns.length < numLikertQs || shortAns.length < numShortAnsQs) {
        console.error('There is an unanswered question. Please report this error to the experimenter.');
        console.error('Collected answers: ', sid, likertAns, shortAns);
    } else {
        localStorage.setItem('doneSurvey', JSON.stringify({
            value: true
        }));
        var currStage = localStorage.getItem('currStage');
        var completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
        var currPart = completedParts[completedParts.length - 1];
        var isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;

        // TODO: store survey data!!! 
        // --> Make sure it's stored wrt currStage (novice/adv)
        // --> Make sure it's stored wrt currPart (v,t,v+t)
        console.error('Survey data is not being stored. TODO: store data!!');

        // getNextStageUrl is found in stages-process.js
        var url = getNextStageUrl(currStage, completedParts, true, isAdvanced);
        window.open(url, '_self');
    }
};

var createDOM = () => {
    // Create the survey
    var currStage = localStorage.getItem('currStage');
    var completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
    var currPart = completedParts[completedParts.length - 1];

    var system = '';
    var verbage = '';
    var finalSurvey = false;
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

    // #1: add heading
    var info = document.getElementById("info");
    if (!finalSurvey) {
        info.innerHTML = '<h2>' + (system.charAt(0).toUpperCase() + system.substring(1)) +
            '-based System Survey</h2>' + '<h3>' + (currStage.charAt(0).toUpperCase() +
                currStage.substring(1)) + ' Stage</h3>' + '<p>How strongly do you agree ' +
            'with the following statements with regards to your experience with the <strong>' +
            system + '-based</strong> system (i.e., the ' + verbage + ' system)?' + '</p>';
    } else {
        // final survey
        info.innerHTML = '<h2>System Comparison Survey</h2>' + '<p>How strongly do you prefer ' +
            'each system compared to the others?</p>';
    }
    info.innerHTML += '<div id="likert-wrap">' + '<form id="likert-form"></form></div>';
    var form = document.getElementById('likert-form');

    // #2: add the likert scale questions
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
    var likertQs = [];
    var labels = [];
    var values = [];
    if (!finalSurvey) {
        likertQs = ['I found it difficult to complete the goal with the ' + system +
            '-based system.', 'I found programming with the ' + system + '-based system difficult to use.',
            'I am satisfied programming with the ' + system + '-based system.',
            'I found programming with the ' + system + '-based system efficient to use.'
        ];
        // all the same labels/values for each question, in this case:
        likertQs.forEach(function () {
            labels.push(['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree']);
            values.push(['strongly_agree', 'Agree', 'neutral', 'disagree', 'strongly_disagree']);
        });
    } else {
        // I preferred: text ←------→ voice (5-point slider)
        // I preferred: voice ←------→ voice+text (5-point slider)
        // I preferred: voice+text ←------→ text (5-point slider)
        labels = [
            ['Text-based system strongly', 'Text-based system', 'Either system', 'Voice-based system', 'Voice-based system strongly'],
            ['Voice-based system strongly', 'Voice-based system', 'Either system', 'Voice/text-based system', 'Voice/text-based system strongly'],
            ['Voice/text-based system strongly', 'Voice/text-based system', 'Either system', 'Text-based system', 'Text-based system strongly']
        ];

        // all the same questions (and values, to make analysis easier) in this case:
        labels.forEach(function () {
            likertQs.push('I preferred:');
            values.push(['strongly_agree', 'Agree', 'neutral', 'disagree', 'strongly_disagree']);
        });
    }

    // store the total number of likertQ's s.t. we can check if all are completed later:
    localStorage.setItem('numLikertQs', likertQs.length);

    // programmatically create the likert scale questions
    // per question ~ i
    // per radio button ~ j
    for (var i = 0; i < likertQs.length; i++) {
        form.innerHTML += '<label class="statement">' + likertQs[i] + '</label>';
        form.innerHTML += '<ul class=\'likert answer\' id="l' + i + '"></ul>';
        var ul = document.getElementById('l' + i);

        for (var j = 0; j < labels[i].length; j++) {
            var li = document.createElement("LI");
            var input = document.createElement("input");
            input.type = "radio";
            input.name = "l" + i;
            input.value = values[i][j];
            var label = document.createElement("label");
            label.innerHTML = labels[i][j];
            li.appendChild(input);
            li.appendChild(label);
            ul.appendChild(li);
        }
    }


    // #3: add headings
    // <h2>Voice-based System Survey</h2>
    // <h3>Novice Stage</h3>
    // <p>
    //     Answer the following questions with regards to your experience with the
    //     <strong>voice-based</strong> system (i.e., the speaking-only system).
    // </p>
    form.innerHTML += '<h2>' + (system.charAt(0).toUpperCase() + system.substring(1)) +
        '-based System Survey</h2>' + '<h3>' + (currStage.charAt(0).toUpperCase() +
            currStage.substring(1)) + ' Stage</h3>' + '<p>Answer the following questions ' +
        'with regards to your experience with the <strong>' + system +
        '-based</strong> system (i.e., the ' + verbage + ' system)?' + '</p>';


    // #4: add the short answer questions
    // E.g.,
    // <label class="statement">
    //     What did you like about programming with the voice-based system?
    // </label>
    // <textarea class="answer" id="s1" type="text" placeholder="I liked..."></textarea>
    var shortAnsQs = ['What did you like about programming with the ' + system + '-based system?',
        'What was frustrating about programming with the ' + system + '-based system? ' +
        'How could we make it less frustrating?', 'What did you wish you could say to the agent? ' +
        'What didn’t the agent understand?', 'What features can we add, change, or remove to make ' +
        'the system better?'
    ];
    var placeholders = ['I liked...', 'You could improve the system by...',
        'I wish I could have said things like...', 'You could add...'
    ];

    // store the total number of shortAnsQ's s.t. we can check if all are completed later:
    localStorage.setItem('numShortAnsQs', shortAnsQs.length);

    for (var i = 0; i < shortAnsQs.length; i++) {
        form.innerHTML += '<label class="statement">' + shortAnsQs[i] +
            '</label>' + '<textarea class="answer" id="s' + i +
            '" type="text" placeholder="' + placeholders[i] +
            '"></textarea>';
    }

    // #5: add the 'next' button
    // <div id="button-container">
    //     <button type="button" class="btn btn-primary submit" id="btn-next">
    //         Next
    //     </button>
    // </div>
    form.innerHTML += '<div id="button-container">' + '<button type="button"' +
        ' class="btn btn-primary submit" id="btn-next"> Next</button></div>';
};