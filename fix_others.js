const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

// Fix deleteSet
js = js.replace(/async function deleteSet\(\) \{[\s\S]*?deleteTarget = null;\n\}/s,
`async function deleteSet() {
    if (!deleteTarget) return;
    closeDeleteModal();
    showSplashScreen();
    
    const payload = {
        action: 'delete',
        rowIndex: deleteTarget.rowIndex
    };
    
    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        
        if (result.status === 'success') {
            showToast('Deleted');
            fetchData();
        } else {
            showToast('Error: ' + result.message);
        }
    } catch (e) {
        console.error(e);
        hideSplashScreen();
        showToast('Error deleting record');
    }
    
    deleteTarget = null;
}`);

// Fix renderStats
js = js.replace(/filteredData\.forEach\(d => \{[\s\S]*?\}\);/s,
`filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = { sets: [] };
        dailyTotals[d.dateStr].sets.push(d.reps);
        
        const sum = d.reps;
        grandTotal += sum;
        
        const dDate = new Date(d.dateStr);
        if (dDate >= weekStart && dDate < weekEnd) {
            weeklyTotal += sum;
            weeklyDaysSet.add(d.dateStr);
        }
        
        if (d.dateStr === todayStr) {
            todayTotal += sum;
            todaySetsCount += 1;
        }
    });`);

fs.writeFileSync('app.js', js, 'utf8');
