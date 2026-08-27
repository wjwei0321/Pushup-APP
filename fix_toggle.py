import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_toggle = '''function toggleChartType(type) {
    currentStatsChartType = type;
    renderStats();
}'''

new_toggle = '''function toggleChartType() {
    currentStatsChartType = currentStatsChartType === 'line' ? 'bar' : 'line';
    localStorage.setItem('pushup_statsChartType', currentStatsChartType);
    renderStats();
}'''

js = js.replace(old_toggle, new_toggle)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
