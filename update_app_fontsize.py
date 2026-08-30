import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change interval growth font size to 22px
js = js.replace('font-size: 1.25rem;', 'font-size: 22px;')

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
