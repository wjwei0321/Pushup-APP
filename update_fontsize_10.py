import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change interval growth font size to 10px
js = js.replace('font-size: 22px; letter-spacing: 0.5px;', 'font-size: 10px; letter-spacing: 0.5px;')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
