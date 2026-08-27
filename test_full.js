const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');

const dom = new JSDOM(html, { 
    runScripts: 'dangerously', 
    pretendToBeVisual: true 
});

dom.window.Chart = class Chart { constructor() { this.ctx = {}; this.scales = {}; } };

dom.window.onerror = function(msg, url, line, col, error) {
    console.error("WINDOW ONERROR:", msg, line, col);
};
dom.window.console.error = function(...args) {
    console.error("CONSOLE ERROR:", ...args);
};

try {
    dom.window.eval(js);
    console.log('JS parsed and ran synchronously.');
    
    // Simulate DOMContentLoaded
    dom.window.document.dispatchEvent(new dom.window.Event('DOMContentLoaded'));
    console.log('DOMContentLoaded fired.');
    
} catch(e) {
    console.error('CATCH:', e);
}
