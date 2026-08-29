import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """async function confirmDeleteSet(rowIndex) {
    rowIndex = parseInt(rowIndex);
    const entryIndex = trainingData.findIndex(d => d.rowIndex === rowIndex || parseInt(d.rowIndex) === rowIndex);
    if (entryIndex === -1) return;
    
    if (confirm(`Delete this record?`)) {
        showSplashScreen();
        // Optimistic UI update
        trainingData.splice(entryIndex, 1);
        renderDailyLog();
        renderCalendar();
        
        const payload = {
            action: 'delete',
            rowIndex: rowIndex
        };
        try {
            const res = await fetch(apiUrl, { 
                method: 'POST', 
                redirect: 'follow',
                headers: {
                    'Content-Type': 'text/plain;charset=utf-8',
                },
                body: JSON.stringify(payload) 
            });
            const result = await res.json();
            if (result.status === 'success') {
                showToast('Deleted');
            } else {
                showToast('Error: ' + result.message);
            }
        } catch (e) {
            console.error(e);
            showToast('Error');
        } finally {
            hideSplashScreen();
            fetchData();
        }
    } else {
        renderDailyLog();
    }
}"""

js = re.sub(
    r"async function confirmDeleteSet\(rowIndex\) \{.*?(?=async function updateSetOnBackend)",
    replacement + "\n\n",
    js,
    flags=re.DOTALL
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
