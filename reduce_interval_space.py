import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace ` &nbsp;` with ` `
js = js.replace("&nbsp;${signPct}", " ${signPct}")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
