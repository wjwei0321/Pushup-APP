const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

const regex = /function renderHomeExerciseGrid\(\) \{[\s\S]*?\}\n    \n    let filteredData =/m;
const match = js.match(regex);
if (match) {
    const fnBody = match[0].replace('    \n    let filteredData =', '');
    js = js.replace(fnBody, '');
    js += '\n' + fnBody;
    fs.writeFileSync('app.js', js);
    console.log('Fixed syntax!');
} else {
    console.log('Still no match');
}
