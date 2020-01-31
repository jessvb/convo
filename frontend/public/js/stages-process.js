// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
    var currStage = localStorage.getItem('currStage');
    var completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
    var isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;
    
    var nextBtn = document.getElementById('btn-next-stage');
    nextBtn.addEventListener('click', function(){
        var url = getNextStageUrl(currStage, completedParts, isAdvanced);
        window.open(url, '_self');
    });
});

/**
 * Returns url of randomly chosen stage (voice/text/voice+text), given completed stages.
 * @param {*} currStage : either 'practice', 'novice', or 'advanced'
 * @param {*} completedParts : either 'voice', 'text', or 'voice-text'
 * "advanced-text", etc.
 * @param {*} isAdvanced : true if the user is an advanced user
 */
function getNextStageUrl (currStage, completedParts, isAdvanced) {
	var url = '';

	if (completedParts.length > 2) {
		// done v, t, v+t for the current stage, so go to the next stage
		switch (currStage) {
			case 'practice':
				url = 'novice-info';
				break;
			case 'novice':
				if (isAdvanced) {
                    url = 'advanced-info';
				} else {
					url = 'conclusion';
				}
				break;
			case 'advanced':
				url = 'conclusion';
			break;
		}
	} else {
		url = currStage + '-';

		let chooseNum = 3 - completedParts.length; // 3 types of stages to choose from (v,t,v+t)
		let uncompletedParts = ['voice', 'text', 'voice-text'];
		if (completedParts.includes('voice')) {
			uncompletedParts.splice(uncompletedParts.indexOf('voice'), 1);
		}
		if (completedParts.includes('text')) {
			uncompletedParts.splice(uncompletedParts.indexOf('text'), 1);
		}
		if (completedParts.includes('voice-text')) {
			uncompletedParts.splice(uncompletedParts.indexOf('voice-text'), 1);
		}

		let rand = Math.floor(Math.random() * chooseNum); // returns a random integer from 0 to chooseNum
		url += uncompletedParts[rand];
	}

	return url;
}