const socket = io.connect("http://userstudy.appinventor.mit.edu:80/");

socket.on('connect', (data) => {
    socket.emit('join', localStorage.getItem("clientId"));
});

socket.on('joined', (data) => {
    localStorage.setItem("clientId", data);
    console.log("Socket connected to server.");
});
