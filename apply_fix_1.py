import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_str = "    const datasets = [];\n    \n    if (currentStatsChartType === 'line') {"
end_str = "    if (statsChartInstance) {\n        statsChartInstance.destroy();\n    }"

start_idx = js.find(start_str)
end_idx = js.find(end_str) + len(end_str)

new_block = """    const datasets = [];
    
    if (sortedDates.length === 0) {
        // Provide dummy data for empty chart
        const now = new Date();
        for(let i=6; i>=0; i--) {
            const d = new Date(now);
            d.setDate(d.getDate() - i);
            labels.push((d.getMonth()+1) + '/' + d.getDate());
        }
        if (currentStatsChartType === 'line') {
            datasets.push({
                label: currentStatsExercise,
                data: [0,0,0,0,0,0,0],
                borderColor: '#e0e0e0',
                backgroundColor: 'transparent',
                fill: false,
                tension: 0,
                borderWidth: 2,
                pointRadius: 0
            });
        } else {
            datasets.push({
                label: currentStatsExercise,
                data: [0,0,0,0,0,0,0],
                backgroundColor: '#e0e0e0',
                borderRadius: 2,
                barPercentage: 0.6
            });
        }
    } else {
        if (currentStatsChartType === 'line') {
            const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets.reduce((a, b) => a + b, 0));
            datasets.push({
                label: currentStatsExercise,
                data: data,
                borderColor: '#f39c12',
                backgroundColor: 'USE_GRADIENT',
                fill: true,
                tension: 0.2,
                borderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 4,
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: '#f39c12',
                pointHoverBorderWidth: 2
            });
        } else {
            const maxSets = Math.max(0, ...Object.values(dailyTotals).map(v => v.sets.length));
            const ORANGE_SHADES = [
                '#ffe5b4', '#ffc87c', '#ffb050', '#ff9500', 
                '#e67e22', '#c75b00', '#a64100', '#852d00', 
                '#631d00', '#421000', '#2b0a00', '#140400'
            ];
            for (let i = 0; i < maxSets; i++) {
                const color = ORANGE_SHADES[i % ORANGE_SHADES.length];
                
                const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets[i] || 0);
                datasets.push({
                    label: `Set ${i + 1}`,
                    data: data,
                    backgroundColor: color,
                    borderRadius: 2,
                    barPercentage: 0.6,
                });
            }
        }
    }
    
    const ctx = document.getElementById('statsChart').getContext('2d');
    
    let isUpdate = false;
    if (statsChartInstance && statsChartInstance.config.type === currentStatsChartType) {
        isUpdate = true;
    } else if (statsChartInstance) {
        statsChartInstance.destroy();
    }"""

js = js[:start_idx] + new_block + js[end_idx:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
