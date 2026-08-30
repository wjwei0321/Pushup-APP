import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("font-weight: 800; font-size: 1.25rem;", "font-weight: 500; font-size: 1.25rem;")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
