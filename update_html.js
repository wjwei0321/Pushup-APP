const fs = require('fs');

let html = fs.readFileSync('index.html', 'utf8');

// 1. Remove the entire block for API URL input
html = html.replace(/<label style="display: block; font-weight: 600; margin-bottom: 8px; font-size: 0\.9rem;">API URL.*?<\/button>/s, `<button onclick="saveSettings()" style="width: 100%; padding: 16px; border-radius: 14px; border: none; background: #111; color: white; font-family: Outfit; font-weight: 700; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">Save & Sync</button>`);

// 2. Bump version
html = html.replace(/v=4\.28/g, 'v=4.29');

fs.writeFileSync('index.html', html, 'utf8');
