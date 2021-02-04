// This file contains methods to control all of the surveys during the experiment

// Once the DOM has finished loading, do stuff:
document.addEventListener('DOMContentLoaded', (event) => {
	// focus on the first input element
	if (document.getElementsByClassName('answer').item(0)) {
		document.getElementsByClassName('answer').item(0).focus();
	}

	// disable the submit button:
	setSubmitBtn('answer');

	// make the submit button pass the userID onto the experiment page (when
	// enabled) by adding an event listener (to all submit buttons)
	let btns = document.getElementsByClassName('submit');
	for (let i = 0; i < btns.length; i++) {
		let btn = btns[i];
		btn.onclick = submitAndGo;
	}

	// add event listener for keystroke etc. such that we can tell if the user has
	// entered information into the input boxes before submitting
	// get all input boxes, check if they all have values
	// enable or disable the submit button:
	document.oninput = () => setSubmitBtn('answer');

	// This ensures the radio button changes also trigger setSubmitBtn
	document.onchange = () => setSubmitBtn('answer');
});

/**
 * Enable or disable a submit button depending on whether the inputs have values
 * entered or not.
 *
 * @param {String} inputClassName: a string containing the class name of the inputs
 *                      you want to check to see if they have value entered
 */
let setSubmitBtn = (inputClassName) => {
	let button = getVisibleSubmitBtn();
	// check if there's a visible submit button on the page (if not, don't do
	// anything)
	if (button != null) {
		// Assume the form is completed, check each input element and set
		// formCompleted = false if one of the elements has no value (and is
		// visible)
		let inputs = document.getElementsByClassName(inputClassName);
		let formCompleted = true;
		for (let i = 0; i < inputs.length; i++) {
			let input = inputs.item(i);

			// if input is visible, then check whether there is user input in the
			// input
			if (isVisible(input)) {
				// check if there are sub-items with inputs (meaning that there are
				// probably radio buttons)
				let subElms = input.getElementsByTagName('input');
				if (subElms.length > 0 && subElms.item(0).type == 'radio') {
					// radio button input is more difficult to check b/c you have to loop
					// through all radio buttons with the same name and check if one of
					// them is selected. Thus, let's use the method 'getSelectedRadio' to
					// do so:
					let radioGroupName = subElms.item(0).name;
					if (getSelectedRadio(radioGroupName) == null) {
						// there aren't any radio buttons selected in this group.
						// The form isn't complete.
						formCompleted = false;
						break;
					}

				} else {
					// check non-radio button input types
					if (!input.value || input.value == 'select') {
						formCompleted = false;
						break;
					}
				}
			}
		}

		// enable/disable submit btn
		button.disabled = !formCompleted;
	}
};

/**
 * Returns the submit button that is visible in the DOM (or null if no visible
 * submit buttons).
 */
let getVisibleSubmitBtn = () => {
	let visBtn;
	let btns = document.getElementsByClassName('submit');
	// find visible submit button
	for (let i = 0; i < btns.length; i++) {
		let btn = btns[i];
		if (isVisible(btn)) {
			visBtn = btn;
			// there should only be a single submit button visible, so break
			break;
		}
	}
	return visBtn;
};

/**
 * Get the selected radio button value. Returns null if none selected.
 */
let getSelectedRadio = (radioGroupName) => {
	let radios = document.getElementsByName(radioGroupName);
	let selectedVal = null;
	for (let i = 0; i < radios.length; i++) {
		if (radios[i].checked) {
			selectedVal = radios[i].value;
			// don't bother checking the rest, since only one can be selected
			break;
		}
	}
	return selectedVal;
};

/**
 * Returns true if the provided element is visible in the DOM.
 */
let isVisible = (htmlElement) => !(htmlElement.offsetParent == null);
