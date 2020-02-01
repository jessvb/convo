// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    // Create the survey
    // #1: add the likert scale questions
    // TODO
    // #2: add the short answer questions
    // TODO
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
    for (let i = 1; i <= 4; i++) {
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