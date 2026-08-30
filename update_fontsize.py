import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Change statsTodayLabel and statsWeeklyLabel font size to 28px
html = html.replace('font-size: 0.82rem; color: #f39c12;', 'font-size: 28px; color: #f39c12;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
