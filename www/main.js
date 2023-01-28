// read query string for connectTo argument
var urlParams = new URLSearchParams(window.location.search);

/** @type string */
var connectTo = urlParams.get('connectTo') || location.host


var ws = new WebSocket(`ws://${connectTo}/`);
var messages = document.createElement('ul');

ws.onmessage = function (event) {
	var messages = document.getElementsByTagName('ul')[0],
		message = document.createElement('li'),
		content = document.createTextNode(event.data);
	message.appendChild(content);
	messages.appendChild(message);
};
document.body.appendChild(messages);

/**  @type {{[key:string}:bool}} */
var keystate = {};

var keybind = {
	forward: 'KeyW',
	backward: 'KeyS',
	left: 'KeyA',
	right: 'KeyD'
}

/**
 * 
 * @param {KeyboardEvent} e 
 */
function onKeyDown(e) {
	switch (e.code) {
		case 'KeyW':
		case 'KeyS':
		case 'KeyA':
		case 'KeyD':
			keystate[e.code] = true;
			update(true)
			e.preventDefault()
	}
}

/**
 * 
 * @param {KeyboardEvent} e 
 */
function onKeyUp(e) {
	switch (e.code) {
		case 'KeyW':
		case 'KeyS':
		case 'KeyA':
		case 'KeyD':
			keystate[e.code] = false;
			update(true)
			e.preventDefault()
	}
}


/**
 * @param {PointerEvent} e 
 */
function onButtonDown(e) {
	this.setPointerCapture(e.pointerId);
	keystate[this.id] = true;
	update(true)
	e.preventDefault()
}

/**
 * @param {PointerEvent} e 
 */
function onButtonUp(e) {
	keystate[this.id] = false;
	update(true)
	e.preventDefault()
}


// reverse map from  socketserver.py
const opmap = { forward: 1, backward: 2, left: 3, right: 4, stop: 5 }

/**
 * 
 * @param {keyof opmap} op 
 */
function sendOp(op) {
	ws.send(new Int8Array([opmap[op]]))
	opcodeDisplay.innerText = op
}
/** @type {HTMLElement} */
var opcodeDisplay = document.getElementById("opcode")

/** @param isEvent: boolean */
function update(isEvent) {
	// multiple keys pressend not supported. will just take these in order
	for (let k in opmap) {
		if (keystate[keybind[k]]) {
			sendOp(k)
			return;
		}
	}
	// if nothing was sent. stop (only if this is result of a keypress)
	// this is to allow multiple connections to the same device to work without stopping all the time
	if (isEvent === true)
		sendOp('stop')
}

document.onkeydown = onKeyDown
document.onkeyup = onKeyUp


for (let arr of document.getElementsByClassName("arr")) {
	/** {HTMLDivElement} */
	var a = arr;
	a.addEventListener("pointerdown", onButtonDown)
	a.addEventListener("pointerup", onButtonUp)

	// prevent long press right-click emulation from kicking in, causing the button to skick and the context menu to show up.
	a.addEventListener("contextmenu", function (e) { e.preventDefault(); })
}

// setup and active update loop, so that we can keep actively sending keys.
// the robot stops after 1 second of not receiving messages. 
setInterval(update, 500)