import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Revert .modal back to rgba(0, 0, 0, 0.4)
css = re.sub(
    r'\.modal\s*\{[^}]*background:\s*transparent;',
    lambda m: m.group(0).replace('background: transparent', 'background: rgba(0, 0, 0, 0.4)'),
    css
)

# Add #addWorkoutModal specific rule
if '#addWorkoutModal { background: transparent; }' not in css:
    css += '\n#addWorkoutModal { background: transparent; }\n'

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
