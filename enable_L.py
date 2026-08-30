import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = """    // Interval Comparison Logic (First Day vs Last Day)
    const compContainer = document.getElementById('statsIntervalComparison');
    if (compContainer) {
        if (currentStatsRange === 'L') {
            compContainer.innerHTML = '';
        } else {
            const sortedDatesForComp = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
            let firstDayReps = 0;
            let lastDayReps = 0;
            
            if (sortedDatesForComp.length > 1) {
                const firstDay = sortedDatesForComp[0];
                const lastDay = sortedDatesForComp[sortedDatesForComp.length - 1];
                firstDayReps = dailyTotals[firstDay].sets.reduce((sum, val) => sum + val, 0);
                lastDayReps = dailyTotals[lastDay].sets.reduce((sum, val) => sum + val, 0);
                
                const diff = lastDayReps - firstDayReps;
                const sign = diff > 0 ? '+' : '';
                const pct = firstDayReps === 0 ? 100 : (diff / firstDayReps * 100);
                const pctStr = firstDayReps === 0 ? '100' : Math.abs(pct).toFixed(1);
                
                let color = '#999';
                let signPct = '';
                if (diff > 0) {
                    color = '#e74c3c'; // Growth = Red
                    signPct = '+';
                } else if (diff < 0) {
                    color = '#2ecc71'; // Decrease = Green
                    signPct = '-';
                }
                
                compContainer.innerHTML = `<span style="color: ${color}; font-weight: 500; font-size: 22px; letter-spacing: 0.5px; font-family: Outfit;">${sign}${diff.toLocaleString()} &nbsp;${signPct}${pctStr}%</span>`;
            } else {
                compContainer.innerHTML = '';
            }
        }
    }"""

new_logic = """    // Interval Comparison Logic (First Day vs Last Day)
    const compContainer = document.getElementById('statsIntervalComparison');
    if (compContainer) {
        const sortedDatesForComp = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
        let firstDayReps = 0;
        let lastDayReps = 0;
        
        if (sortedDatesForComp.length > 1) {
            const firstDay = sortedDatesForComp[0];
            const lastDay = sortedDatesForComp[sortedDatesForComp.length - 1];
            firstDayReps = dailyTotals[firstDay].sets.reduce((sum, val) => sum + val, 0);
            lastDayReps = dailyTotals[lastDay].sets.reduce((sum, val) => sum + val, 0);
            
            const diff = lastDayReps - firstDayReps;
            const sign = diff > 0 ? '+' : '';
            const pct = firstDayReps === 0 ? 100 : (diff / firstDayReps * 100);
            const pctStr = firstDayReps === 0 ? '100' : Math.abs(pct).toFixed(1);
            
            let color = '#999';
            let signPct = '';
            if (diff > 0) {
                color = '#e74c3c'; // Growth = Red
                signPct = '+';
            } else if (diff < 0) {
                color = '#2ecc71'; // Decrease = Green
                signPct = '-';
            }
            
            compContainer.innerHTML = `<span style="color: ${color}; font-weight: 500; font-size: 22px; letter-spacing: 0.5px; font-family: Outfit;">${sign}${diff.toLocaleString()} &nbsp;${signPct}${pctStr}%</span>`;
        } else {
            compContainer.innerHTML = '';
        }
    }"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
