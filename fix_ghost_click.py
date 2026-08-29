import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# We need to remove the touchstart and mousedown from dismissHandler.
# Let's find this block:
#         modal.addEventListener('mousedown', dismissHandler);
#         modal.addEventListener('touchstart', dismissHandler, {passive: true});

js = re.sub(
    r'modal\.addEventListener\(\'mousedown\', dismissHandler\);\s*modal\.addEventListener\(\'touchstart\', dismissHandler, \{passive: true\}\);',
    r'modal.addEventListener(\'click\', dismissHandler);',
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
