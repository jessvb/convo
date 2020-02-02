const socket = io.connect("https://userstudy.appinventor.mit.edu");
const socketApi = io.connect("https://userstudy.appinventor.mit.edu", { path: '/api/socket.io' })

socketApi.on('connect', (data) => {
    socketApi.emit('join', { "sid": localStorage.getItem("sid"), "stage": localStorage.getItem("currStage")});
});

socketApi.on('joined', (data) => {
    localStorage.setItem("sid", data);
    console.log("Socket connected to API server.");
});

socket.on('connect', (data) => {
    socket.emit('join', localStorage.getItem("cid"));
});

socket.on('joined', (data) => {
    localStorage.setItem("cid", data);
    console.log("Socket connected to server.");
});

socket.on('streamError', (err) => {
    console.log(err);
});
