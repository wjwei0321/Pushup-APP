import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Find the datasets push logic
old_code = """    if (currentStatsChartType === 'line') {
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
            pointHoverBorderWidth: 2,
            pointHitRadius: 10
        });
    } else {
        const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets.reduce((a, b) => a + b, 0));
        datasets.push({
            label: currentStatsExercise,
            data: data,
            backgroundColor: '#f39c12',
            borderRadius: 4,
            barThickness: 'flex',
            maxBarThickness: 40
        });
    }"""

new_code = """    if (sortedDates.length === 0) {
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
                backgroundColor: '#e0e0e0'
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
                pointHoverBorderWidth: 2,
                pointHitRadius: 10
            });
        } else {
            const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets.reduce((a, b) => a + b, 0));
            datasets.push({
                label: currentStatsExercise,
                data: data,
                backgroundColor: '#f39c12',
                borderRadius: 4,
                barThickness: 'flex',
                maxBarThickness: 40
            });
        }
    }"""

js = js.replace(old_code, new_code)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
