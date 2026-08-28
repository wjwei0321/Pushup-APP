const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

const regex = /function renderHomeExerciseGrid\(\) \{[\s\S]*?\}\n\n/g;
js = js.replace(regex, '');
js = js.replace(/    renderHomeExerciseGrid\(\);\n/g, '');

fs.writeFileSync('app.js', js);
