import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_open = """function openSettings() {
    document.getElementById('userEmail').value = userEmail;"""
new_open = """function openSettings() {
    if (document.getElementById('apiUrl')) document.getElementById('apiUrl').value = apiUrl;
    document.getElementById('userEmail').value = userEmail;"""

js = js.replace(old_open, new_open)

old_save = """function saveSettings() {
    const apiVal = document.getElementById('apiUrl').value.trim();
    const emailVal = document.getElementById('userEmail').value.trim();"""
new_save = """function saveSettings() {
    const apiEl = document.getElementById('apiUrl');
    const apiVal = apiEl ? apiEl.value.trim() : '';
    const emailVal = document.getElementById('userEmail').value.trim();"""

js = js.replace(old_save, new_save)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
