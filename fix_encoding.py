import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("firstDayReps === 0 ? '' :", "firstDayReps === 0 ? '100' :")
js = js.replace("firstDayReps === 0 ? '∞' :", "firstDayReps === 0 ? '100' :")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
