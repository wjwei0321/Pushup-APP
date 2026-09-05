import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace(
    "dateFormatted = dateObj.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });",
    "dateFormatted = dateObj.toLocaleDateString(currentLang === 'zh' ? 'zh-TW' : 'en-US', { month: 'short', day: 'numeric', year: 'numeric' });"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
