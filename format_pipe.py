import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("`Set ${entry.setNumber} | ${entry.time}`", "`Set ${entry.setNumber} ｜ ${entry.time}`")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
