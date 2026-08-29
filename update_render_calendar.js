const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(
    /exerciseSets\[d\.type\] \+= d\.sets\.length;/g,
    "exerciseSets[d.type] += 1;"
);

fs.writeFileSync('app.js', js, 'utf8');
