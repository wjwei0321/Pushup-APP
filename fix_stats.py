import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix todayStr format
js = js.replace(
    "const todayStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;",
    "const todayStr = `${now.getFullYear()}/${String(now.getMonth() + 1).padStart(2, '0')}/${String(now.getDate()).padStart(2, '0')}`;"
)

# Fix sets push
js = js.replace(
    "dailyTotals[d.dateStr].sets.push(...d.sets);",
    "dailyTotals[d.dateStr].sets.push(d.reps || 0);"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
