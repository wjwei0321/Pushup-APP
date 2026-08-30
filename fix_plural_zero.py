import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change `=== 1` to `<= 1`
js = js.replace("weeklyDaysSet.size === 1 ? 'day' : 'days'", "weeklyDaysSet.size <= 1 ? 'day' : 'days'")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
