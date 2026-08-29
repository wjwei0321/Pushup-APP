const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/const apiVal = document\.getElementById\('apiUrl'\)\.value\.trim\(\);\n/, '');
js = js.replace(/    if \(apiVal\) \{\n        apiUrl = apiVal;\n        localStorage\.setItem\('pushup_apiUrl', apiUrl\);\n    \}\n\n/, '');

fs.writeFileSync('app.js', js, 'utf8');
