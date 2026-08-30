import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace font-weight: 600 with font-weight: 500
html = html.replace('font-weight: 600; letter-spacing: 0.2px;', 'font-weight: 500; letter-spacing: 0.2px;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
