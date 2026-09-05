import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# First, undo the replace_file_content I just did
js = js.replace("""    if (statsChartInstance && statsChartInstance.config.type === currentStatsChartType) {
        if (currentStatsChartType === 'line' && datasets.length > 0) {
            datasets[0].borderColor = '#f39c12';
            datasets[0].backgroundColor = (context) => {
                const chart = context.chart;
                const {ctx, chartArea} = chart;
                if (!chartArea) return 'rgba(243, 156, 18, 0.2)';
                const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                gradient.addColorStop(0, 'rgba(243, 156, 18, 0)');
                gradient.addColorStop(0.5, 'rgba(243, 156, 18, 0.15)');
                gradient.addColorStop(1, 'rgba(243, 156, 18, 0.5)');
                return gradient;
            };
        }
        
        statsChartInstance.data.labels = labels;
        statsChartInstance.data.datasets = datasets;
        if (!statsChartInstance.data.customData) statsChartInstance.data.customData = {};
        statsChartInstance.data.customData.sortedDates = sortedDates;
        statsChartInstance.data.customData.dailyTotals = dailyTotals;
        statsChartInstance.update();
    } else {
        if (statsChartInstance) {
            statsChartInstance.destroy();
        }
        
        if (currentStatsChartType === 'line' && datasets.length > 0) {
            datasets[0].borderColor = '#f39c12';
            datasets[0].backgroundColor = (context) => {
                const chart = context.chart;
                const {ctx, chartArea} = chart;
                if (!chartArea) return 'rgba(243, 156, 18, 0.2)'; // fallback before layout
                const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                gradient.addColorStop(0, 'rgba(243, 156, 18, 0)'); // fully transparent at bottom
                gradient.addColorStop(0.5, 'rgba(243, 156, 18, 0.15)'); // smooth transition
                gradient.addColorStop(1, 'rgba(243, 156, 18, 0.5)'); // theme orange at the top
                return gradient;
            };
        }""", """    if (statsChartInstance) {
        statsChartInstance.destroy();
    }
    
    if (currentStatsChartType === 'line' && datasets.length > 0) {
        datasets[0].borderColor = '#f39c12';
        datasets[0].backgroundColor = (context) => {
            const chart = context.chart;
            const {ctx, chartArea} = chart;
            if (!chartArea) return 'rgba(243, 156, 18, 0.2)'; // fallback before layout
            const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
            gradient.addColorStop(0, 'rgba(243, 156, 18, 0)'); // fully transparent at bottom
            gradient.addColorStop(0.5, 'rgba(243, 156, 18, 0.15)'); // smooth transition
            gradient.addColorStop(1, 'rgba(243, 156, 18, 0.5)'); // theme orange at the top
            return gradient;
        };
    }""")

# Let's locate the entire `const ctx = ...` up to the end of `new Chart(...)`
# We'll match `const ctx = document.getElementById('statsChart').getContext('2d');`
# and the end of the `renderStats` function which is `statsChartInstance = new Chart(...) ... });`

# Easiest way is to find the block manually using indices
start_idx = js.find("    const ctx = document.getElementById('statsChart').getContext('2d');\n    if (statsChartInstance) {\n        statsChartInstance.destroy();\n    }")

# Find the end of `statsChartInstance = new Chart(ctx, {`
# Which ends at `});` right before `const todayLabel = document.getElementById('statsTodayLabel');`? No, wait.
# Let's find `statsChartInstance = new Chart(ctx, {`
chart_start = js.find("    statsChartInstance = new Chart(ctx, {", start_idx)

# Find the matching `});` for the chart
chart_end = js.find("    });", chart_start) + len("    });")

original_block = js[start_idx:chart_end]

new_block = """    const ctx = document.getElementById('statsChart').getContext('2d');
    
    if (statsChartInstance && statsChartInstance.config.type === currentStatsChartType) {
        if (currentStatsChartType === 'line' && datasets.length > 0) {
            datasets[0].borderColor = '#f39c12';
            datasets[0].backgroundColor = (context) => {
                const chart = context.chart;
                const {ctx, chartArea} = chart;
                if (!chartArea) return 'rgba(243, 156, 18, 0.2)';
                const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                gradient.addColorStop(0, 'rgba(243, 156, 18, 0)');
                gradient.addColorStop(0.5, 'rgba(243, 156, 18, 0.15)');
                gradient.addColorStop(1, 'rgba(243, 156, 18, 0.5)');
                return gradient;
            };
        }
        
        statsChartInstance.data.labels = labels;
        statsChartInstance.data.datasets = datasets;
        if (!statsChartInstance.data.customData) statsChartInstance.data.customData = {};
        statsChartInstance.data.customData.sortedDates = sortedDates;
        statsChartInstance.data.customData.dailyTotals = dailyTotals;
        statsChartInstance.update();
    } else {
""" + original_block.replace("    const ctx = document.getElementById('statsChart').getContext('2d');\n", "").replace("\n", "\n    ") + "\n    }"

js = js[:start_idx] + new_block + js[chart_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
