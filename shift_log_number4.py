import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace padding: 0 12px 0 0; with padding: 0 9px 0 0;
old_style = "outline: none; padding: 0 12px 0 0;"
new_style = "outline: none; padding: 0 9px 0 0;"

js = js.replace(old_style, new_style)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
