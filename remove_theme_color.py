import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove the whole syncThemeColor block
js = re.sub(
    r'// Sync theme-color with modal state for iOS notch.*?syncThemeColor\(\);',
    '',
    js,
    flags=re.DOTALL
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
