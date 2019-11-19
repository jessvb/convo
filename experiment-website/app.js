const express = require('express');
const app = express();

app.use(express.static('public'));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/OpeningPage.html');
});

app.get('/OpeningSurvey.html', (req, res) => {
    res.sendFile(__dirname + '/OpeningSurvey.html');
});

app.get('/PracticeInfoPage.html', (req, res) => {
    res.sendFile(__dirname + '/PracticeInfoPage.html');
});

app.get('/PracticeTextSystem.html', (req, res) => {
    res.sendFile(__dirname + '/PracticeTextSystem.html');
});

app.listen(3000, () => console.log('Gator app listening on port 3000!'));