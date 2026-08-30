import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace double space with single space
js = js.replace("toLocaleString()}  ${signPct}", "toLocaleString()} ${signPct}")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
