const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

// 1. Hardcode API URL and remove localStorage
js = js.replace(/let apiUrl = localStorage\.getItem\('pushup_apiUrl'\) \|\| '.*?';/, "let apiUrl = 'https://script.google.com/macros/s/AKfycbzygwNK8lzpzJlcFLntcUjhfOiZPQjyHKxssyrjh_pXgVNKd8dSkNrMQSmBCWiP1uG1/exec';");

// 2. Remove apiUrl from saveSettings
js = js.replace(/function saveSettings\(\) \{.*?\n    \}\n/s, `function saveSettings() {
    const emailVal = document.getElementById('userEmail').value.trim();\n`);

// 3. Remove apiUrl from loadSettings (if it exists)
js = js.replace(/const storedApi = localStorage\.getItem\('pushup_apiUrl'\);\n    if \(storedApi\) \{\n        document\.getElementById\('apiUrl'\)\.value = storedApi;\n    \}/, "");

fs.writeFileSync('app.js', js, 'utf8');
