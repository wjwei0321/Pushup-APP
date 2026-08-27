const html = require('fs').readFileSync('index.html', 'utf8');
const lines = html.split('\n');
let count = 0;
for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const opens = (line.match(/<div/g) || []).length;
    const closes = (line.match(/<\/div>/g) || []).length;
    count += opens - closes;
    if (count < 0) {
        console.log('Negative count at line ' + (i+1) + ': ' + line);
        break;
    }
}
console.log('Final count:', count);
