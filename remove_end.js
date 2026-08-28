const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

const regex = /function renderHomeExerciseGrid\(\) \{[\s\S]*\}\s*$/m;
js = js.replace(regex, '');

fs.writeFileSync('app.js', js);
