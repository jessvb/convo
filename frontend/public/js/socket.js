// const socket = io.connect("https://userstudy.appinventor.mit.edu");
const socketApi = io.connect("http://localhost:5000");
const socket = io.connect("http://localhost:8080");

socketApi.on('connect', (data) => {
    socketApi.emit('join', localStorage.getItem("sid"));
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
