const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(/function confirmDeleteSet\(rowIndex\) \{[\s\S]*?async function updateSetOnBackend/s,
`async function confirmDeleteSet(rowIndex) {
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    if (confirm('Delete this record?')) {
        showSplashScreen();
        const payload = {
            action: 'delete',
            rowIndex: rowIndex
        };
        try {
            const res = await fetch(apiUrl, { method: 'POST', body: JSON.stringify(payload) });
            const result = await res.json();
            if (result.status === 'success') {
                showToast('Deleted');
                fetchData();
            } else {
                showToast('Error');
            }
        } catch (e) {
            hideSplashScreen();
            showToast('Error');
        }
    } else {
        // Snap back
        renderDailyLog();
    }
}

async function updateSetOnBackend`);

fs.writeFileSync('app.js', js, 'utf8');
