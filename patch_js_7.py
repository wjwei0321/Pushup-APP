import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "    renderCalendar();\n    \n    // Refresh Exercise Picker",
    "    renderCalendar();\n    renderDailyLog();\n    \n    // Refresh Exercise Picker"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
