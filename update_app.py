import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Switch View logic
new_switch_view = '''function switchView(viewName) {
    if (viewName === 'stats') {
        const statsView = document.getElementById('statsView');
        statsView.style.display = 'block';
        void statsView.offsetWidth; // reflow
        statsView.style.transform = 'translateY(0)';
        renderStats();
        return;
    }

    const statsView = document.getElementById('statsView');
    statsView.style.transform = 'translateY(100%)';
    setTimeout(() => {
        if (statsView.style.transform === 'translateY(100%)') statsView.style.display = 'none';
    }, 300);

    document.getElementById('homeView').style.display = viewName === 'home' ? 'block' : 'none';
    document.getElementById('calendarView').style.display = viewName === 'calendar' ? 'block' : 'none';
    
    document.querySelectorAll('.floating-nav .nav-item').forEach(item => {
        item.classList.remove('active');
    });
    
    if (viewName === 'home') {
        document.querySelectorAll('.floating-nav .nav-item')[0].classList.add('active');
        renderLogList();
    } else if (viewName === 'calendar') {
        document.querySelectorAll('.floating-nav .nav-item')[2].classList.add('active');
        renderCalendar();
    }
}'''

js = re.sub(r'function switchView\(viewName\) \{.*?\}', new_switch_view, js, flags=re.DOTALL)

# 2. Bottom Icons logic (make them circles and fit 8 in a row)
new_icon_logic = '''        const iconWrap = document.createElement('div');
        // Fit 8 in a row: padding and width must be tight
        iconWrap.style.cssText = 'width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; padding: 6px; cursor: pointer; transition: all 0.2s; flex-shrink: 0;';
        if (currentStatsExercise === ex) {
            iconWrap.style.background = '#f39c12';
            iconWrap.style.color = '#fff';
            iconWrap.style.boxShadow = '0 2px 8px rgba(243,156,18,0.4)';
        } else {
            iconWrap.style.background = '#f5f5f5';
            iconWrap.style.color = '#999';
            iconWrap.style.boxShadow = 'none';
        }'''

js = re.sub(r"        const iconWrap = document.createElement\('div'\);\s*iconWrap\.style\.cssText = 'min-width: 48px;.*?\} else \{.*?\}", new_icon_logic, js, flags=re.DOTALL)

# 3. Chart styling (Y-axis on left, maxTicks 3, pill background)
crosshair_plugin_code = '''    const yAxisPillPlugin = {
        id: 'yAxisPill',
        beforeDraw: (chart) => {
            const ctx = chart.ctx;
            const yAxis = chart.scales.y;
            ctx.save();
            ctx.fillStyle = 'rgba(0, 0, 0, 0.05)';
            yAxis.getTicks().forEach((tick, index) => {
                const y = yAxis.getPixelForTick(index);
                ctx.beginPath();
                ctx.roundRect(10, y - 10, 36, 20, 10);
                ctx.fill();
            });
            ctx.restore();
        }
    };

    const crosshairPlugin = {'''

js = js.replace("    const crosshairPlugin = {", crosshair_plugin_code)
js = js.replace("plugins: [crosshairPlugin]", "plugins: [crosshairPlugin, yAxisPillPlugin]")

# 4. Chart scales updates for Light Theme and Y-axis Left
new_scales = '''            scales: {
                x: {
                    stacked: currentStatsChartType === 'bar',
                    grid: { display: false },
                    border: { display: false },
                    ticks: {
                        maxTicksLimit: 6,
                        font: { family: 'Outfit', size: 10, weight: '500' },
                        color: '#999',
                        padding: 10
                    }
                },
                y: {
                    position: 'left',
                    stacked: currentStatsChartType === 'bar',
                    beginAtZero: true,
                    border: { display: false },
                    grid: { 
                        color: '#f0f0f0',
                        drawBorder: false,
                    },
                    ticks: {
                        maxTicksLimit: 3,
                        font: { family: 'Outfit', size: 10, weight: '600' },
                        color: '#666',
                        padding: 0,
                        mirror: true, // Draws labels inside the chart area, overlapping it
                        z: 10, // Bring labels above the grid
                        callback: function(value) {
                            return '  ' + value; // Add small indent so it sits nicely inside the pill
                        }
                    }
                }
            }'''

js = re.sub(r'            scales: \{.*?                \}\s*\}', new_scales, js, flags=re.DOTALL)

# Update tooltip colors for light theme
js = js.replace("backgroundColor: '#1a1e26'", "backgroundColor: '#fff'")
js = js.replace("titleColor: '#787b86'", "titleColor: '#999'")
js = js.replace("bodyColor: '#fff'", "bodyColor: '#333'")
js = js.replace("borderColor: '#2a2e39'", "borderColor: '#eee'")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
