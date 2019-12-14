const socket = io.connect("https://userstudy.appinventor.mit.edu");

socket.on('connect', (data) => {
    socket.emit('join', localStorage.getItem("clientId"));
});

socket.on('joined', (data) => {
    localStorage.setItem("clientId", data);
    console.log("Socket connected to server.");
});
