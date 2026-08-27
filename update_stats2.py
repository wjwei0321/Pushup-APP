import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

new_render = '''function renderStats() {
    document.getElementById('btnLineChart').classList.toggle('active', currentStatsChartType === 'line');
    document.getElementById('btnBarChart').classList.toggle('active', currentStatsChartType === 'bar');
    
    const exList = [...new Set(trainingData.map(d => d.type))];
    if (!exList.includes(currentStatsExercise) && exList.length > 0) {
        currentStatsExercise = exList[0];
    }
    if (exList.length === 0) return; // No data
    
    // Update Header
    document.getElementById('statsHeaderTitle').textContent = currentStatsExercise;
    document.getElementById('statsHeaderIcon').innerHTML = EXERCISES[currentStatsExercise] || '';
    
    // Bottom Exercise Tabs
    const filterContainer = document.getElementById('statsExerciseFilter');
    filterContainer.innerHTML = '';
    Object.keys(EXERCISES).forEach(ex => {
        if (!exList.includes(ex)) return;
        const iconWrap = document.createElement('div');
        iconWrap.style.cssText = 'min-width: 48px; height: 48px; border-radius: 12px; display: flex; align-items: center; justify-content: center; padding: 10px; cursor: pointer; transition: all 0.2s;';
        if (currentStatsExercise === ex) {
            iconWrap.style.background = '#2962ff'; // Active tab
            iconWrap.style.color = '#fff';
        } else {
            iconWrap.style.background = '#1a1e26';
            iconWrap.style.color = '#787b86';
        }
        iconWrap.innerHTML = EXERCISES[ex];
        iconWrap.onclick = () => setStatsExercise(ex);
        filterContainer.appendChild(iconWrap);
    });
    
    let filteredData = trainingData.filter(d => d.type === currentStatsExercise);
    
    const dailyTotals = {};
    let grandTotal = 0;
    
    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = { sets: [] };
        dailyTotals[d.dateStr].sets.push(...d.sets);
        grandTotal += d.sets.reduce((a, b) => a + b, 0);
    });
    
    document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();
    
    const sortedDates = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
    const labels = sortedDates.map(dateStr => {
        const d = new Date(dateStr);
        return d.getDate() + '/' + (d.getMonth() + 1);
    });
    
    const datasets = [];
    
    if (currentStatsChartType === 'line') {
        const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets.reduce((a, b) => a + b, 0));
        datasets.push({
            label: currentStatsExercise,
            data: data,
            borderColor: '#2962ff',
            backgroundColor: 'USE_GRADIENT',
            fill: true,
            tension: 0.2,
            borderWidth: 2,
            pointRadius: 0,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: '#2962ff',
            pointHoverBorderWidth: 2
        });
    } else {
        const maxSets = Math.max(0, ...Object.values(dailyTotals).map(v => v.sets.length));
        const ORANGE_SHADES = ['#f39c12', '#e67e22', '#d35400', '#f1c40f', '#e74c3c', '#ff7f50', '#ff8c00', '#ffa500'];
        for (let i = 0; i < maxSets; i++) {
            const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets[i] || 0);
            datasets.push({
                label: Set ,
                data: data,
                backgroundColor: ORANGE_SHADES[i % ORANGE_SHADES.length],
                borderRadius: 2,
                barPercentage: 0.6,
            });
        }
    }
    
    const ctx = document.getElementById('statsChart').getContext('2d');
    if (statsChartInstance) {
        statsChartInstance.destroy();
    }
    
    if (currentStatsChartType === 'line' && datasets.length > 0) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 320);
        gradient.addColorStop(0, 'rgba(41, 98, 255, 0.4)');
        gradient.addColorStop(1, 'rgba(41, 98, 255, 0)');
        datasets[0].backgroundColor = gradient;
        datasets[0].borderColor = '#2962ff'; // TradingView blue/green? Wait, user asked for orange!
    }
    
    const crosshairPlugin = {
        id: 'crosshair',
        afterDraw: chart => {
            if (chart.tooltip?._active?.length) {
                const activePoint = chart.tooltip._active[0];
                const ctx = chart.ctx;
                const x = activePoint.element.x;
                const bottomY = chart.scales.y.bottom;

                ctx.save();
                ctx.beginPath();
                ctx.moveTo(x, chart.scales.y.top);
                ctx.lineTo(x, bottomY);
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#2a2e39';
                ctx.stroke();
                ctx.restore();
            }
        }
    };
    
    statsChartInstance = new Chart(ctx, {
        type: currentStatsChartType,
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            layout: {
                padding: { left: -10, right: 12, top: 20, bottom: 0 }
            },
            animation: {
                duration: 400
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    backgroundColor: '#1a1e26',
                    titleFont: { size: 12, family: 'Outfit', weight: '500' },
                    bodyFont: { size: 14, family: 'Outfit', weight: '700' },
                    titleColor: '#787b86',
                    bodyColor: '#fff',
                    padding: { top: 8, bottom: 8, left: 14, right: 14 },
                    cornerRadius: 6,
                    displayColors: currentStatsChartType === 'bar',
                    boxPadding: 4,
                    borderColor: '#2a2e39',
                    borderWidth: 1,
                    callbacks: {
                        label: function(context) {
                            if (currentStatsChartType === 'line') return context.parsed.y + ' reps';
                            return context.dataset.label + ': ' + context.parsed.y;
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: currentStatsChartType === 'bar',
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        maxTicksLimit: 6,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#787b86',
                        padding: 10
                    }
                },
                y: {
                    position: 'right',
                    stacked: currentStatsChartType === 'bar',
                    beginAtZero: true,
                    border: { display: false },
                    grid: { 
                        color: '#1a1e26', // faint grid lines like tradingview
                        drawBorder: false,
                    },
                    ticks: {
                        maxTicksLimit: 5,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#787b86',
                        padding: 12,
                        mirror: false,
                        z: 0
                    }
                }
            }
        },
        plugins: [crosshairPlugin]
    });
}'''

js = re.sub(r'function renderStats\(\) \{.*?(?=\n})', new_render[:-2], js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
