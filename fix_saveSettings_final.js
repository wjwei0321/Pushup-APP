const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/function saveSettings\(\) \{[\s\S]*?fetchData\(\);\n\}/s,
`function saveSettings() {
    const emailVal = document.getElementById('userEmail').value.trim();
    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }
    settingsModal.classList.remove('show');
    setTimeout(() => { settingsModal.style.display = 'none'; }, 300);
    showSplashScreen();
    fetchData();
}`);

fs.writeFileSync('app.js', js, 'utf8');
