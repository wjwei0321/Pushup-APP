import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to inject the logic for statsIntervalComparison right after we calculate grandTotal
# In renderStats:
#     document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();
#     
#     const todayLabel = document.getElementById('statsTodayLabel');
#     ...

logic = """    document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();
    
    // Interval Comparison Logic
    const compContainer = document.getElementById('statsIntervalComparison');
    if (compContainer) {
        if (currentStatsRange === 'L') {
            compContainer.innerHTML = '';
        } else {
            const fullDataForEx = trainingData.filter(d => d.type === currentStatsExercise);
            const now = new Date();
            const cutoffDate = new Date();
            const prevCutoffDate = new Date();
            
            if (currentStatsRange === 'S') {
                cutoffDate.setMonth(now.getMonth() - 3);
                prevCutoffDate.setMonth(now.getMonth() - 6);
            } else if (currentStatsRange === 'M') {
                cutoffDate.setMonth(now.getMonth() - 6);
                prevCutoffDate.setMonth(now.getMonth() - 12);
            }
            
            let previousPeriodSum = 0;
            fullDataForEx.forEach(d => {
                const dDate = new Date(d.dateStr);
                if (dDate >= prevCutoffDate && dDate < cutoffDate) {
                    previousPeriodSum += (d.reps || 0);
                }
            });
            
            const currentPeriodSum = grandTotal;
            
            if (previousPeriodSum === 0 && currentPeriodSum === 0) {
                compContainer.innerHTML = '';
            } else {
                const diff = currentPeriodSum - previousPeriodSum;
                const sign = diff > 0 ? '+' : '';
                const pct = previousPeriodSum === 0 ? 100 : (diff / previousPeriodSum * 100);
                const pctStr = previousPeriodSum === 0 ? '∞' : Math.abs(pct).toFixed(1);
                
                // Growth = Red (#e74c3c), Decrease = Green (#2ecc71)
                let color = '#999';
                let signPct = '';
                if (diff > 0) {
                    color = '#e74c3c';
                    signPct = '+';
                } else if (diff < 0) {
                    color = '#2ecc71';
                    signPct = '-';
                }
                
                compContainer.innerHTML = `<span style="color: ${color}; font-weight: 800; font-size: 1.25rem; letter-spacing: 0.5px; font-family: Outfit;">${sign}${diff.toLocaleString()} &nbsp;${signPct}${pctStr}%</span>`;
            }
        }
    }
"""

js = js.replace("    document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();", logic)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
