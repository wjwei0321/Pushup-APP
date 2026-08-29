import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace button and add version
html = re.sub(
    r'(<button onclick="saveSettings\(\)".*?>Save & Sync</button>)',
    r'\1\n                <div style="margin-top: 20px; text-align: center; font-size: 0.8rem; color: var(--text-secondary);">API V5 &nbsp;|&nbsp; APP 4.45</div>',
    html
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
