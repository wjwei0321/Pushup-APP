import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the label replacement in exercise picker
js = js.replace(
    "label.innerHTML = t(ex).replace(' ', '<br>'); // Simple wrap for long names if needed, but zh is short",
    "label.innerHTML = (currentLang === 'en' && ex === 'Polyquin Step-down') ? 'Polyquin<br>Step-down' : t(ex);"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
