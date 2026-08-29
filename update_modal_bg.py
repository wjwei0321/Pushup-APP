import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

css = re.sub(
    r'\.modal\s*\{[^}]*background:\s*rgba\(0,\s*0,\s*0,\s*0\.4\);',
    lambda m: m.group(0).replace('rgba(0, 0, 0, 0.4)', 'transparent'),
    css
)

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
