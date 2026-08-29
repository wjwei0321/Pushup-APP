import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Settings & Profile -> Profile
html = html.replace('>Settings & Profile</h3>', '>Profile</h3>')

# 2. Your Email (for sync) -> Email
html = html.replace('>Your Email (for sync)</label>', '>Email</label>')

# 3. Add version text at the bottom of the modal, before the Save button or at the bottom.
# Let's put it below the Save button.
version_html = '''
            <button onclick="saveSettings()" style="width: 100%; padding: 16px; background: var(--primary); color: white; border: none; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer;">Save & Sync</button>
            <div style="margin-top: 20px; text-align: center; font-size: 0.8rem; color: var(--text-secondary);">API V5 &nbsp;|&nbsp; APP 4.45</div>
'''
html = html.replace('<button onclick="saveSettings()" style="width: 100%; padding: 16px; background: var(--primary); color: white; border: none; border-radius: 12px; font-size: 1.1rem; font-weight: 600; cursor: pointer;">Save & Sync</button>', version_html)

# Update cache buster
html = html.replace('v=4.44', 'v=4.45')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Update Logged in as + Color
js = js.replace("userDisplay.textContent = 'Logged in as: ' + (json.username || userEmail);", "userDisplay.textContent = (json.username || userEmail);")
js = js.replace("userDisplay.style.color = '#34c759';", "userDisplay.style.color = '#ff9500';")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
