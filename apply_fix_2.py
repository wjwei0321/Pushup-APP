import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_str = "    statsChartInstance = new Chart(ctx, {"
chart_start = js.find(start_str)
chart_end = js.find("    });", chart_start) + len("    });")

original_chart = js[chart_start:chart_end]

new_chart = """    if (isUpdate) {
        statsChartInstance.data.labels = labels;
        statsChartInstance.data.datasets = datasets;
        if (!statsChartInstance.data.customData) statsChartInstance.data.customData = {};
        statsChartInstance.data.customData.sortedDates = sortedDates;
        statsChartInstance.data.customData.dailyTotals = dailyTotals;
        statsChartInstance.update();
    } else {
""" + original_chart.replace("\n", "\n    ") + """
    }"""

js = js[:chart_start] + new_chart + js[chart_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
