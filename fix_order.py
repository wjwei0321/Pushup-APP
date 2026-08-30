import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_btns = """<div class="range-toggle-btn active" data-range="L" onclick="setStatsRange('L')">L</div>
                    <div class="range-toggle-btn" data-range="M" onclick="setStatsRange('M')">M</div>
                    <div class="range-toggle-btn" data-range="S" onclick="setStatsRange('S')">S</div>"""

new_btns = """<div class="range-toggle-btn" data-range="S" onclick="setStatsRange('S')">S</div>
                    <div class="range-toggle-btn" data-range="M" onclick="setStatsRange('M')">M</div>
                    <div class="range-toggle-btn active" data-range="L" onclick="setStatsRange('L')">L</div>"""

html = html.replace(old_btns, new_btns)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
