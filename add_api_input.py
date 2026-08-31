import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """<div style="margin-top: 20px; text-align: center; font-size: 0.8rem; color: var(--text-secondary);">API V6 &nbsp;|&nbsp; APP 4.91</div>"""
new_html = """<div style="margin-top: 20px; text-align: center; font-size: 0.8rem; color: var(--text-secondary);" onclick="document.getElementById('apiContainer').style.display='block'">API V6 &nbsp;|&nbsp; APP 4.92</div>
                <div id="apiContainer" style="display: none; margin-top: 20px;">
                    <label style="display: block; font-weight: 600; margin-bottom: 8px; font-size: 0.9rem;">API URL</label>
                    <input type="url" id="apiUrl" style="width: 100%; padding: 15px; border-radius: 12px; border: 1.5px solid var(--border-color); background: var(--card-bg); font-family: Outfit; font-size: 0.8rem; box-sizing: border-box;">
                </div>"""

html = html.replace(old_html, new_html)

# Also bump the top scripts
html = html.replace('app.js?v=4.91', 'app.js?v=4.92')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
