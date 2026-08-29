import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """      const payload = {
          action: 'edit',
          email: userEmail,
          rowIndex: entry.rowIndex,
          count: entry.reps
      };"""

js = re.sub(
    r"const payload = \{\s*action: entry\.sets\.length === 0 \? 'delete' : 'edit',\s*email: userEmail,\s*rowIndex: entry\.rowIndex,[^\n]*\s*reps: entry\.sets\s*\};",
    replacement,
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
