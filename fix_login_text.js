const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/if \(json\.username\) \{[\s\S]*?\}\s*\}/,
`const userDisplay = document.getElementById('currentUserDisplay');
            if(userDisplay) {
                userDisplay.textContent = 'Logged in as: ' + (json.username || userEmail);
                userDisplay.style.color = '#34c759';
            }`);

fs.writeFileSync('app.js', js, 'utf8');
