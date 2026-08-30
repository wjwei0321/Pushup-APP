import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

old_html = """                  <div>
                      <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px;">
                          <span style="font-size: 3.2rem; font-weight: 800; color: #111; line-height: 1; letter-spacing: -1.5px;" id="statsTotalNumber">0</span>
                      </div>
                      <div style="display: flex; gap: 16px; align-items: center; min-height: 24px;">
                          <div id="statsTodayLabel" style="font-size: 0.95rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 today</div>
                          <div id="statsWeeklyLabel" style="font-size: 0.95rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 this week</div>
                      </div>
                  </div>"""

new_html = """                  <div style="display: flex; flex-direction: column; gap: 4px;">
                      <div style="display: flex; align-items: baseline; gap: 8px;">
                          <span style="font-size: 3.2rem; font-weight: 800; color: #111; line-height: 1; letter-spacing: -1.5px;" id="statsTotalNumber">0</span>
                      </div>
                      <!-- Interval Comparison -->
                      <div id="statsIntervalComparison" style="min-height: 28px; display: flex; align-items: center;">
                          <!-- JS will inject e.g. <span style="color: #e74c3c; font-weight: 700; font-size: 1.15rem;">+200 +53.2%</span> -->
                      </div>
                      <!-- Weekly/Today Stats -->
                      <div style="display: flex; gap: 16px; align-items: center; min-height: 20px;">
                          <div id="statsTodayLabel" style="font-size: 0.82rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 today</div>
                          <div id="statsWeeklyLabel" style="font-size: 0.82rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px; display: none;">+0 this week</div>
                      </div>
                  </div>"""

html = html.replace(old_html, new_html)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
