import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "headerMonthDayEl.textContent = `${MONTH_NAMES[selectedDate.getMonth()]} ${selectedDate.getDate()}`;",
    "headerMonthDayEl.textContent = selectedDate.toLocaleDateString(currentLang === 'zh' ? 'zh-TW' : 'en-US', { month: 'long', day: 'numeric' });"
)
js = js.replace(
    "const month = MONTH_NAMES[selectedDate.getMonth()].substring(0, 3);\n    selectedDateDisplay.textContent = `${month} ${selectedDate.getDate()}`;",
    "selectedDateDisplay.textContent = selectedDate.toLocaleDateString(currentLang === 'zh' ? 'zh-TW' : 'en-US', { month: 'short', day: 'numeric' });"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
