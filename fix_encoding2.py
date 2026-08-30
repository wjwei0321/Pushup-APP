import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = re.sub(r"firstDayReps === 0 \? '.*?' : Math.abs\(pct\)\.toFixed\(1\)", r"firstDayReps === 0 ? '100' : Math.abs(pct).toFixed(1)", js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
