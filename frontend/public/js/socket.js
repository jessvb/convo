const socket = io.connect("http://0.0.0.0:8080");

socket.on('connect', (data) => {
    socket.emit('join', localStorage.getItem("clientId"));
});

socket.on('joined', (data) => {
    localStorage.setItem("clientId", data);
    console.log("Socket connected to server.");
});
