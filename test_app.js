const fs = require('fs');
const jsdom = require('jsdom');
const { JSDOM } = jsdom;

const html = fs.readFileSync('index.html', 'utf8');
const js = fs.readFileSync('app.js', 'utf8');

const dom = new JSDOM(html, { runScripts: 'dangerously' });

try {
    // We need to mock Chart
    dom.window.Chart = class Chart { constructor() {} };
    dom.window.eval(js);
    console.log('No global syntax/runtime errors on load!');
} catch(e) {
    console.error('ERROR ON LOAD:', e);
}
