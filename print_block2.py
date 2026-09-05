import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_str = "    if (currentStatsChartType === 'line' && datasets.length > 0) {"
end_str = "    });\n    \n    const yAxisPillPlugin"

start_idx = js.find(start_str)
end_idx = js.find(end_str)

if end_idx == -1:
    # try to find the end of the chart instantiation
    chart_start = js.find("statsChartInstance = new Chart(ctx, {")
    end_idx = js.find("    });", chart_start) + len("    });")

original_block = js[start_idx:end_idx]
print(original_block[:200] + "\n...\n" + original_block[-200:])
