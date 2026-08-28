const fs = require('fs');
let js = fs.readFileSync('app.js', 'utf8');
const index = js.indexOf('\n else {');
if (index !== -1) {
    js = js.substring(0, index);
    fs.writeFileSync('app.js', js);
    console.log('Fixed syntax error.');
} else {
    console.log('Could not find garbage code.');
}
