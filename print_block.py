import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_str = "    const datasets = [];\n    \n    if (currentStatsChartType === 'line') {"
end_str = "    if (statsChartInstance) {\n        statsChartInstance.destroy();\n    }"

start_idx = js.find(start_str)
end_idx = js.find(end_str) + len(end_str)

original_block = js[start_idx:end_idx]
print(original_block)
