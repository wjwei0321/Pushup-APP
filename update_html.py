import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_stats_view = '''    <!-- Stats View (TradingView Style) -->
    <div id="statsView" class="view-container" style="display: none; padding-bottom: 100px; background: #0b0e14; color: #fff; min-height: 100vh;">
        <div style="padding: calc(20px + env(safe-area-inset-top, 20px)) 24px 0 24px;">
            <!-- TradingView Header -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                <div style="display: flex; gap: 12px; align-items: center;">
                    <div id="statsHeaderIcon" style="width: 42px; height: 42px; background: #1a1e26; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #f39c12; padding: 8px;">
                        <!-- Icon injected via JS -->
                    </div>
                    <div style="display: flex; flex-direction: column;">
                        <span id="statsHeaderTitle" style="font-size: 1.2rem; font-weight: 700; letter-spacing: -0.5px; color: #e0e3eb;">Exercise</span>
                        <span style="font-size: 0.75rem; color: #787b86; font-weight: 600; letter-spacing: 0.5px;">STE ¡E WORKOUT  <span style="color: #26a69a;">¡´</span><span style="color: #2962ff;">¡´</span><span style="color: #e91e63;">¡´</span></span>
                    </div>
                </div>
                
                <!-- Chart Toggles -->
                <div style="display: flex; gap: 6px;">
                    <div id="btnLineChart" class="stats-toggle-btn active" onclick="toggleChartType('line')" style="background: #1a1e26; color: #787b86; border: none; border-radius: 8px; width: 36px; height: 36px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                    </div>
                    <div id="btnBarChart" class="stats-toggle-btn" onclick="toggleChartType('bar')" style="background: #1a1e26; color: #787b86; border: none; border-radius: 8px; width: 36px; height: 36px;">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-4"></path></svg>
                    </div>
                </div>
            </div>

            <!-- Big Number -->
            <div style="margin-bottom: 32px;">
                <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px;">
                    <span style="font-size: 3.2rem; font-weight: 800; color: #ffffff; line-height: 1; letter-spacing: -1.5px;" id="statsTotalNumber">0</span>
                    <span style="font-size: 1rem; color: #787b86; font-weight: 600;">REPS</span>
                </div>
                <div style="font-size: 0.95rem; color: #26a69a; font-weight: 600; letter-spacing: 0.2px;">+ RECORD TODAY</div>
            </div>
        </div>

        <!-- Chart Container Full Width -->
        <div style="width: 100%; height: 320px; position: relative; border-top: 1px dashed #2a2e39; border-bottom: 1px dashed #2a2e39;">
            <canvas id="statsChart"></canvas>
        </div>

        <!-- Exercise Icon Bottom Bar -->
        <div style="padding: 24px 0;">
            <div id="statsExerciseFilter" style="display: flex; gap: 16px; overflow-x: auto; padding: 0 24px; scrollbar-width: none;">
                <!-- Icons injected via JS -->
            </div>
        </div>
    </div>'''

html = re.sub(r'    <!-- Stats View -->.*?    <!-- Floating Bottom Navigation -->', new_stats_view + '\n\n    <!-- Floating Bottom Navigation -->', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
