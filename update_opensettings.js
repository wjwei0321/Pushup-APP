const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/document\.getElementById\('apiUrl'\)\.value = apiUrl;\n/, "");

fs.writeFileSync('app.js', js, 'utf8');
