// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
	var currStage = localStorage.getItem('currStage');
	var completedParts = JSON.parse(localStorage.getItem('completedParts')).parts;
	var doneSurvey = JSON.parse(localStorage.getItem('doneSurvey')).value;
	var isAdvanced = JSON.parse(localStorage.getItem('isAdvanced')).value;

	var nextBtn = document.getElementById('btn-next-stage');
	if (nextBtn) {
		nextBtn.addEventListener('click', function () {
			var url = getNextStageUrl(currStage, completedParts, doneSurvey, isAdvanced);
			window.open(url, '_self');
		});
	}
});

/**
 * Returns url of randomly chosen stage (voice/text/voice+text), given completed stages.
 * @param {*} currStage : either 'practice', 'novice', 'advanced', or 'finalSurvey'
 * @param {*} completedParts : either 'voice', 'text', or 'voice-text'
 * "advanced-text", etc.
 * @param {*} doneSurvey : boolean of whether the user completed the survey for this part
 * @param {*} isAdvanced : true if the user is an advanced user
 */
function getNextStageUrl(currStage, completedParts, doneSurvey, isAdvanced) {
	var url = '';

	if (currStage == 'finalSurvey') {
		url = 'conclusion';
	} else if (doneSurvey) {
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
						// final survey
						url = 'comparison-survey';
					}
					break;
				case 'advanced':
					// final survey
					url = 'comparison-survey';
					break;
				default:
					console.error('Current stage not recognized: ' + currStage);
			}
		} else {
			// not done at least one of v, t or v+t
			// randomly choose one of the remaining v,t,v+t to go to next
			url = getRandPartUrl(currStage, completedParts);
		}
	} else {
		// not done survey
		// go to survey based on currStage and last completed part
		switch (currStage) {
			case 'practice':
				// there is no survey after practice, so get a random practice stage:
				url = getRandPartUrl(currStage, completedParts);
				// if getRandPartUrl returns null, then we're done practice stage!
				if (url == null) {
					// go to novice
					url = 'novice-info';
				}
				break;
			case 'novice':
			case 'advanced':
				// if we haven't started any parts, get a random part to start:
				if (completedParts.length < 1) {
					url = getRandPartUrl(currStage, completedParts);
				} else {
					var currPart = completedParts[completedParts.length - 1];
					url = currStage + '-' + currPart + '-survey';
				}
				break;
			default:
				console.error('Current stage not recognized: ' + currStage);
		}

	}

	return url;
}

/**
 * Helper function to get a random part, wrt completed parts and current stage.
 * If there's no parts left to complete, it returns null.
 */
function getRandPartUrl(currStage, completedParts) {
	var url = currStage + '-';

	// get a list of *uncompleted parts* so we can choose from them
	var chooseNum = 3 - completedParts.length; // 3 types of stages to choose from (v,t,v+t)
	var uncompletedParts = ['voice', 'text', 'voice-text'];
	if (completedParts.includes('voice')) {
		uncompletedParts.splice(uncompletedParts.indexOf('voice'), 1);
	}
	if (completedParts.includes('text')) {
		uncompletedParts.splice(uncompletedParts.indexOf('text'), 1);
	}
	if (completedParts.includes('voice-text')) {
		uncompletedParts.splice(uncompletedParts.indexOf('voice-text'), 1);
	}

	// if there's no parts left to complete, return null
	if (uncompletedParts.length < 1) {
		url = null;
	} else {
		var rand = Math.floor(Math.random() * chooseNum); // returns a random integer from 0 to chooseNum
		url += uncompletedParts[rand];
	}
	return url;
}