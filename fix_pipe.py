import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the garbled character with the standard pipe symbol ' | '
js = re.sub(r'Set \$\{entry\.setNumber\}[^$]+\$\{entry\.time\}', r'Set ${entry.setNumber} | ${entry.time}', js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
