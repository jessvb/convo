// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    // Create the survey
    // #1: add heading
    // TODO: get real currStage etc.
    // var currStage = localStorage.getItem('currStage');
    // var currPart = JSON.parse(localStorage.getItem('completedParts')).parts.pop();
    var currStage = 'novice';
    var currPart = ['voice-text', 'text', 'voice'].pop();

    var system = '';
    var verbage = '';
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

    var info = document.getElementById("info");
    info.innerHTML = '<h2>' + (system.charAt(0).toUpperCase() + system.substring(1)) +
        '-based System Survey</h2>' + '<h3>' + (currStage.charAt(0).toUpperCase() +
            currStage.substring(1)) + ' Stage</h3>' + '<p>How strongly do you agree ' +
        'with the following statements with regards to your experience with the <strong>' +
        system + '-based</strong> system (i.e., the ' + verbage + ' system)?' + '</p>';
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
    var likertQs = ['I found it difficult to complete the goal with the ' + system +
        '-based system.', 'I found programming with the ' + system + '-based system difficult to use.',
        'I am satisfied programming with the ' + system + '-based system.',
        'I found programming with the ' + system + '-based system efficient to use.'
    ];

    for (var i = 0; i < likertQs.length; i++) {
        form.innerHTML += '<label class="statement">' + likertQs[i] + '</label>';
        form.innerHTML += '<ul class=\'likert answer\' id="l' + i + '"></ul>';
        var ul = document.getElementById('l' + i);
        var labels = ['Strongly agree', 'Agree', 'Neutral', 'Disagree', 'Strongly disagree'];
        var values = ['strongly_agree', 'Agree', 'neutral', 'disagree', 'strongly_disagree'];
        for (var j = 0; j < labels.length; j++){
            var li = document.createElement("LI");
            var input = document.createElement("input");
            input.type = "radio";
            input.name = "l" + i;
            input.value = values[j];
            var label = document.createElement("label");
            label.innerHTML = labels[j];
            li.appendChild(input);
            li.appendChild(label);
            ul.appendChild(li);
        }
        // var li1 = document.createElement("LI")
        // .appendChild(document.createElement('label').innerHTML = 'Strongly agree');
        // var li2 = document.createElement("LI");
        // var li3 = document.createElement("LI");
        // var li4 = document.createElement("LI");
        // var li5 = document.createElement("LI");
        // // ul.appendChild(li1);
        // ul.appendChild(li2);
        // ul.appendChild(li3);
        // ul.appendChild(li4);
        // ul.appendChild(li5);
        // ul.innerHTML += '<li><input type="radio" name="l' + i +
        //     '" value="strong_agree">' + '<label>Strongly agree</label></li>';
        // ul.innerHTML += '<ul class=\'likert answer\' id="l' + i + '">' +
        //     '<li><input type="radio" name="l' + i + '" value="agree">' +
        //     '<label>Agree</label></li>';
        // ul.innerHTML += '<ul class=\'likert answer\' id="l' + i + '">' +
        //     '<li><input type="radio" name="l' + i + '" value="neutral">' +
        //     '<label>Neutral</label></li>';
        // ul.innerHTML += '<ul class=\'likert answer\' id="l' + i + '">' +
        //     '<li><input type="radio" name="l' + i + '" value="disagree">' +
        //     '<label>Disagree</label></li>';
        // ul.innerHTML += '<ul class=\'likert answer\' id="l' + i + '">' +
        //     '<li><input type="radio" name="l' + i + '" value="strong_disagree">' +
        //     '<label>Strongly disagree</label></li>';
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


    // TODO
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

});

/**
 * Submits the relevant variables from the form to the Google form and goes to
 * the next page.
 */
let submitAndGo = () => {
    // Get the user id for this computer and person:
    let sid = localStorage.getItem('sid');

    let shortAns = [];
    let likertAns = [];
    for (let i = 0; i < 4; i++) {
        shortAns.push(document.getElementById('s' + i).value);
        let radios = document.getElementsByName('l' + i);
        radios.forEach(radio => {
            if (radio.checked) {
                likertAns.push(radio.value);
            }
        });
    }

    console.log('sshort aans: ', shortAns);
    console.log('likert ans: ', likertAns);

    if (sid == null || likertAns.length < 4 || shortAns.length < 4) {
        console.error('There is an unanswered question. Please report this error to the experimenter.');
        console.error('Collected answers: ', sid, likertAns, shortAns);
    } else {
        // TODO: store survey data!!!
        // let url = 'practice-info'; // TODO set url correctly
        // window.open(url, '_self');
    }
};