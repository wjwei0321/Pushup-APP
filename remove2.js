const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/function renderHomeExerciseGrid\(\) \{[\s\S]*?\}\n?/g, '');
js = js.replace(/[ \t]*renderHomeExerciseGrid\(\);\n?/g, '');

fs.writeFileSync('app.js', js);
