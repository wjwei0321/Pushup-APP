const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/function updateSetOnBackend\(entry\) \{[\s\S]*?\}\);[\n\s]*\}/s,
`function updateSetOnBackend(entry) {
    showSplashScreen();
    const payload = {
        action: 'edit',
        rowIndex: entry.rowIndex,
        count: entry.reps
    };
    
    fetch(apiUrl, {
        method: 'POST',
        body: JSON.stringify(payload)
    }).then(r => r.json()).then(res => {
        if(res.status === 'success') {
            showToast('Saved');
            fetchData();
        } else {
            showToast('Error');
            fetchData();
        }
    }).catch(e => {
        hideSplashScreen();
        showToast('Error');
    });
}`);

fs.writeFileSync('app.js', js, 'utf8');
