import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Modify statsIntervalComparison styling
old_div = '<div id="statsIntervalComparison" style="min-height: 28px; display: flex; align-items: center;">'
new_div = '<div id="statsIntervalComparison" style="min-height: 16px; display: flex; align-items: center; margin-top: -4px;">'

html = html.replace(old_div, new_div)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
