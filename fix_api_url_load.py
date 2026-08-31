import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_code = "let apiUrl = 'https://script.google.com/macros/s/AKfycbyfRhXDcH_Sp-IvRU_V4ENJpzWOsoDF2RURchZUpTQ97fxjlDXIOJCJJOOXkjPXnxLJ/exec';"
new_code = "let apiUrl = localStorage.getItem('pushup_apiUrl') || 'https://script.google.com/macros/s/AKfycbyfRhXDcH_Sp-IvRU_V4ENJpzWOsoDF2RURchZUpTQ97fxjlDXIOJCJJOOXkjPXnxLJ/exec';"

js = js.replace(old_code, new_code)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
