import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Make them slightly larger and gap larger
html = html.replace('width: 22px;', 'width: 28px;')
html = html.replace('height: 22px;', 'height: 28px;')
html = html.replace('font-size: 0.65rem;', 'font-size: 0.8rem;')
html = html.replace('background: transparent;', 'background: white;')
html = html.replace('gap: 6px;', 'gap: 12px;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
