const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

// We just want to extract fetchData and see if it throws on valid data
const script = `
const userEmail = "atw007wj@gmail.com";
const apiUrl = "https://script.google.com/macros/s/AKfycbzygwNK8lzpzJlcFLntcUjhfOiZPQjyHKxssyrjh_pXgVNKd8dSkNrMQSmBCWiP1uG1/exec";

function hideSplashScreen() {}
function openSettings() {}
function showToast(msg) { console.log("TOAST:", msg); }
function renderCalendar() {}
function renderDailyLog() {}

const document = {
    getElementById: (id) => { return { textContent: '', style: {} }; }
};

let trainingData = [];

` + js.match(/async function fetchData\(\) \{[\s\S]*?\}\n/)[0] + `

fetchData().then(() => console.log(trainingData)).catch(e => console.error("FATAL ERROR", e));
`;

fs.writeFileSync('test_fetch.js', script);
