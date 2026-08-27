import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to replace renderStats completely
new_render_stats = '''function renderStats() {
    // 1. Update UI active states
    document.querySelectorAll('.stats-time-filter .time-filter-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tf-' + currentStatsTimeFilter)?.classList.add('active');
    
    document.getElementById('btnLineChart').classList.toggle('active', currentStatsChartType === 'line');
    document.getElementById('btnBarChart').classList.toggle('active', currentStatsChartType === 'bar');
    
    // 2. Render Exercise Filter Pills
    const filterContainer = document.getElementById('statsExerciseFilter');
    const allEx = [...new Set(trainingData.map(d => d.type))];
    const exList = ['All', ...allEx];
    
    if (!exList.includes(currentStatsExercise)) {
        currentStatsExercise = 'All';
    }
    
    filterContainer.innerHTML = '';
    exList.forEach(ex => {
        const pill = document.createElement('div');
        pill.className = 'stats-exercise-pill' + (currentStatsExercise === ex ? ' active' : '');
        pill.textContent = ex === 'All' ? '¥þ³¡' : ex;
        pill.onclick = () => setStatsExercise(ex);
        filterContainer.appendChild(pill);
    });
    
    // 3. Filter data by date and exercise
    const now = new Date();
    let cutoffDate = new Date(0);
    if (currentStatsTimeFilter === '3M') {
        cutoffDate = new Date(now.getFullYear(), now.getMonth() - 3, now.getDate());
    } else if (currentStatsTimeFilter === '6M') {
        cutoffDate = new Date(now.getFullYear(), now.getMonth() - 6, now.getDate());
    } else if (currentStatsTimeFilter === '1Y') {
        cutoffDate = new Date(now.getFullYear() - 1, now.getMonth(), now.getDate());
    }
    
    let filteredData = trainingData.filter(d => new Date(d.dateStr) >= cutoffDate);
    
    if (currentStatsExercise !== 'All') {
        filteredData = filteredData.filter(d => d.type === currentStatsExercise);
    }
    
    // 4. Aggregate Data by Date
    const dailyTotals = {};
    let grandTotal = 0;
    
    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = {};
        const sum = d.sets.reduce((a, b) => a + b, 0);
        dailyTotals[d.dateStr][d.type] = (dailyTotals[d.dateStr][d.type] || 0) + sum;
        grandTotal += sum;
    });
    
    document.getElementById('statsTotalNumber').textContent = grandTotal.toLocaleString();
    
    // 5. Prepare Chart.js datasets
    const sortedDates = Object.keys(dailyTotals).sort((a, b) => new Date(a) - new Date(b));
    const labels = sortedDates.map(dateStr => {
        const d = new Date(dateStr);
        return d.getDate() + '/' + (d.getMonth() + 1);
    });
    
    const datasets = [];
    const CHART_COLORS = [
        '#111111', '#3498db', '#e74c3c', '#2ecc71', '#9b59b6'
    ];
    
    if (currentStatsExercise !== 'All') {
        const data = sortedDates.map(dateStr => dailyTotals[dateStr][currentStatsExercise] || 0);
        datasets.push({
            label: currentStatsExercise,
            data: data,
            borderColor: '#111',
            backgroundColor: 'USE_GRADIENT',
            fill: currentStatsChartType === 'line',
            tension: 0.4,
            borderWidth: currentStatsChartType === 'line' ? 3 : 0,
            pointRadius: 0,
            pointHoverRadius: 6,
            pointHoverBackgroundColor: '#c8f560', // Neon green accent like reference
            pointHoverBorderColor: '#111',
            pointHoverBorderWidth: 2,
            borderRadius: currentStatsChartType === 'bar' ? 6 : 0,
            barPercentage: 0.6,
        });
    } else {
        allEx.forEach((ex, i) => {
            const c = CHART_COLORS[i % CHART_COLORS.length];
            const data = sortedDates.map(dateStr => dailyTotals[dateStr][ex] || 0);
            datasets.push({
                label: ex,
                data: data,
                borderColor: c,
                backgroundColor: currentStatsChartType === 'line' ? 'transparent' : c,
                fill: false,
                tension: 0.4,
                borderWidth: currentStatsChartType === 'line' ? 2.5 : 0,
                pointRadius: 0,
                pointHoverRadius: 5,
                pointHoverBackgroundColor: c,
                pointHoverBorderColor: '#fff',
                pointHoverBorderWidth: 2,
                borderRadius: currentStatsChartType === 'bar' ? 6 : 0,
                barPercentage: 0.6,
            });
        });
    }
    
    // 6. Render Chart
    const ctx = document.getElementById('statsChart').getContext('2d');
    if (statsChartInstance) {
        statsChartInstance.destroy();
    }
    
    // Create gradient
    if (currentStatsExercise !== 'All' && currentStatsChartType === 'line' && datasets.length > 0) {
        const gradient = ctx.createLinearGradient(0, 0, 0, 300);
        gradient.addColorStop(0, 'rgba(0, 0, 0, 0.4)');
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');
        datasets[0].backgroundColor = gradient;
        datasets[0].borderColor = '#333';
    }
    
    // Custom vertical line plugin
    const crosshairPlugin = {
        id: 'crosshair',
        afterDraw: chart => {
            if (chart.tooltip?._active?.length) {
                const activePoint = chart.tooltip._active[0];
                const ctx = chart.ctx;
                const x = activePoint.element.x;
                const topY = chart.scales.y.top;
                const bottomY = chart.scales.y.bottom;

                ctx.save();
                ctx.beginPath();
                ctx.moveTo(x, activePoint.element.y);
                ctx.lineTo(x, bottomY);
                ctx.lineWidth = 1;
                ctx.strokeStyle = 'rgba(0, 0, 0, 0.2)';
                ctx.setLineDash([4, 4]);
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
                padding: { left: -10, right: 0, top: 20, bottom: 0 } // Full width bleed
            },
            interaction: {
                mode: 'index',
                intersect: false,
            },
            plugins: {
                legend: {
                    display: currentStatsExercise === 'All' && allEx.length > 1,
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        pointStyle: 'circle',
                        boxWidth: 6,
                        padding: 20,
                        font: { family: 'Outfit', size: 12, weight: '600' },
                        color: '#666'
                    }
                },
                tooltip: {
                    backgroundColor: '#111',
                    titleFont: { size: 11, family: 'Outfit', weight: '500' },
                    bodyFont: { size: 14, family: 'Outfit', weight: '700' },
                    titleColor: 'rgba(255,255,255,0.6)',
                    bodyColor: '#fff',
                    padding: { top: 8, bottom: 8, left: 12, right: 12 },
                    cornerRadius: 8,
                    displayColors: false, // hide color box like reference
                    yAlign: 'bottom', // tooltip floats above point
                    callbacks: {
                        title: () => null, // hide title
                        label: function(context) {
                            return context.parsed.y + ' reps';
                        }
                    }
                }
            },
            scales: {
                x: {
                    stacked: currentStatsChartType === 'bar',
                    grid: { display: false, drawBorder: false },
                    border: { display: false },
                    ticks: {
                        maxTicksLimit: 6,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#999',
                        padding: 10
                    }
                },
                y: {
                    position: 'right',
                    stacked: currentStatsChartType === 'bar',
                    beginAtZero: true,
                    border: { display: false },
                    grid: { display: false, drawBorder: false },
                    ticks: {
                        maxTicksLimit: 5,
                        font: { family: 'Outfit', size: 11, weight: '500' },
                        color: '#999',
                        padding: 10,
                        mirror: true, // Display labels inside the chart area
                        z: 10
                    }
                }
            }
        },
        plugins: [crosshairPlugin]
    });
}'''

js = re.sub(r'function renderStats\(\) \{.*?(?=\n})', new_render_stats[:-2], js, flags=re.DOTALL)
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
