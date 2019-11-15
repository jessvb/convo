/* Copyright (c) 2018 MIT 6.813/6.831 course staff, all rights reserved.
 * Redistribution of original or derived work requires permission of course staff.
 */
class Util {
	/**
	 * Get one element by selector
	 * @param selector {String}
	 * @returns {Element}
	 */
	static one(selector) {
		return document.querySelector(selector);
	}

	/**
	 * Get all elements that match a selector as an array
	 * @param selector {String}
	 * @returns {Array<Element>}
	 */
	static all(selector) {
		return Array.from(document.querySelectorAll(selector));
	}

	/**
	 * Create an element and set a bunch of attributes on it
	 * @param tag {String}
	 * @param attributes {Object}
	 * @returns {Element}
	 */
	static create(tag, attributes) {
		var element = document.createElement(tag);

		for (var name in attributes) {
			element.setAttribute(name, attributes[name]);
		}

		return element;
	}

	/**
	 * Get a parameter from the URL query string
	 * @param name {String}
	 */
	static getURLParam(name) {
		return new URL(location).searchParams.get(name);
	}

	/**
	 * Throws error if passed argument is not a number
	 * @param input {number} Both actual Numbers and numeric strings are accepted
	 * @param errorMsg {String}
	 */
	static assertNumeric(input, errorMsg) {
		if (isNaN(input)) {
			throw errorMsg + ` (Got ${input} instead)`;
		}
	}

	/**
	 * Set a bunch of CSS property-value pairs on one or more elements
	 * Shortcut to avoid a lot of repetitive element.style.prop = value lines
	 * @param element {Element|Array<Element>}
	 * @param declarations {Object}
	 * @returns the same type as 'element', with new styles
	 */
	static css(element, declarations) {
		if (Array.isArray(element)) {
			return element.map(e => Util.css(e, declarations));
		}

		for (var name in declarations) {
			// Why not element.style.propName? To be able to set variables and
			// use normal, hyphenated property names instead of camelCase variants
			element.style.setProperty(name, declarations[name]);
		}

		return element;
	}

	/**
	 * @param delay {number} number of milliseconds
	 * @returns {Promise} gets resolved after the delay
	 */
	static delay(delay) {
		return new Promise(resolve => setTimeout(resolve, delay));
	}

	/**
	 * Set multiple event listeners on an element
	 */
	static events(target, events, callback) {
		if (callback) {
			events.split(/\s+/).forEach(name => target.addEventListener(name, callback));
		}
		else { // Multiple events and callbacks
			for (var name in events) {
				Util.events(target, name, events[name]);
			}
		}
	}

	/**
	 * Returns a promise that is resolved when the event fires
	 * @param target {EventTarget|Array<EventTarget>}
	 * @param eventName {String}
	 * @param test {callback} resolved when the event fires
	 */
	static async when(target, eventName, test = evt => true) {
		if (Array.isArray(target)) {
			return Promise.all(target.map(a => Util.when(a, eventName, test)));
		}

		var callback;
		var evt = await new Promise(resolve => {
			target.addEventListener(eventName, callback = evt => {
				if (test(evt)) {
					resolve(evt);
				}
			});
		});

		target.removeEventListener(eventName, callback);
		return evt;
	}

	/**
	 * Return a promise that is resolved after all animations of a given name
	 * have stopped on one or more elements.
	 * Caveat: The animations need to be *already* applied when this is called.
	 * @param target {Element|Array<Element>}
	 * @param animationName {String}
	 */
	static afterAnimation(target, animationName) {
		target = Array.isArray(target)? target : [target];
		var animating = target.filter(candy => getComputedStyle(candy).animationName.includes(animationName));

		return Promise.all(animating.map(el => Util.when(el, "animationend", evt => evt.animationName == animationName)));
	}

	/**
	 * Get element offsets relative to the document
	 * @param element {Element}
	 */
	static offset(element) {
		var rect = element.getBoundingClientRect();
		var win = element.ownerDocument.defaultView;

		return {
			top: rect.top + win.scrollY,
			left: rect.left + win.scrollX
		};
	}
}
