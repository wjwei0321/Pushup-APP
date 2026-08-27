const css = require('fs').readFileSync('style.css', 'utf8');
let count = 0;
for (let i = 0; i < css.length; i++) {
    if (css[i] === '{') count++;
    if (css[i] === '}') count--;
    if (count < 0) {
        console.log('Negative count at index ' + i);
        break;
    }
}
console.log('Final CSS count:', count);
