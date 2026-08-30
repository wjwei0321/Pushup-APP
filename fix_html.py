import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

def replace_stats_html(match):
    return """                  <div style="display: flex; flex-direction: column; gap: 4px;">
                      <div style="display: flex; align-items: baseline; gap: 8px;">
                          <span style="font-size: 3.2rem; font-weight: 800; color: #111; line-height: 1; letter-spacing: -1.5px;" id="statsTotalNumber">0</span>
                      </div>
                      <!-- Interval Comparison -->
                      <div id="statsIntervalComparison" style="min-height: 28px; display: flex; align-items: center;">
                          <!-- JS will inject -->
                      </div>
                      <div style="display: flex; gap: 16px; align-items: center; min-height: 20px;">
                          <div id="statsTodayLabel" style="font-size: 0.82rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 today</div>
                          <div id="statsWeeklyLabel" style="font-size: 0.82rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 this week</div>
                      </div>
                  </div>"""

# Match from <div> before <div style="...statsTotalNumber... to the end of statsWeeklyLabel div
pattern = r"\s*<div>\s*<div style=\"display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px;\">\s*<span style=\"font-size: 3\.2rem;.*?id=\"statsTotalNumber\">0</span>\s*</div>\s*<div style=\"display: flex; gap: 16px; align-items: center; min-height: 24px;\">\s*<div id=\"statsTodayLabel\".*?</div>\s*<div id=\"statsWeeklyLabel\".*?</div>\s*</div>\s*</div>"

html = re.sub(pattern, replace_stats_html, html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
