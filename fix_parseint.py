import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "rowIndex: rowIndex",
    "rowIndex: parseInt(rowIndex)"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
