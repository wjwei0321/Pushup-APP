import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the statsView HTML
new_stats_view = '''    <!-- Stats View (TradingView Light Style as Modal) -->
    <div id="statsView" style="display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; z-index: 2000; background: var(--bg-color); color: var(--text-primary); transition: transform 0.3s cubic-bezier(0.1, 0.8, 0.3, 1); transform: translateY(100%); overflow-y: auto; padding-bottom: 50px;">
        <!-- Drag Handle -->
        <div id="statsDragHandle" style="width: 100%; padding: 16px 0; display: flex; justify-content: center; touch-action: none;">
            <div style="width: 40px; height: 5px; background: #e0e0e0; border-radius: 3px;"></div>
        </div>
        
        <div style="padding: 0 24px;">
            <!-- TradingView Header -->
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 24px;">
                <div style="display: flex; gap: 12px; align-items: center;">
                    <div id="statsHeaderIcon" style="width: 42px; height: 42px; background: #f5f5f5; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: #f39c12; padding: 8px;">
                        <!-- Icon injected via JS -->
                    </div>
                    <div style="display: flex; flex-direction: column;">
                        <span id="statsHeaderTitle" style="font-size: 1.2rem; font-weight: 700; letter-spacing: -0.5px; color: var(--text-primary);">Exercise</span>
                        <span style="font-size: 0.75rem; color: #999; font-weight: 600; letter-spacing: 0.5px;">STE ¡E WORKOUT</span>
                    </div>
                </div>
            </div>

            <!-- Big Number -->
            <div style="margin-bottom: 32px;">
                <div style="display: flex; align-items: baseline; gap: 8px; margin-bottom: 4px;">
                    <span style="font-size: 3.2rem; font-weight: 800; color: var(--text-primary); line-height: 1; letter-spacing: -1.5px;" id="statsTotalNumber">0</span>
                    <span style="font-size: 1rem; color: #999; font-weight: 600;">REPS</span>
                </div>
                <div style="font-size: 0.95rem; color: #f39c12; font-weight: 600; letter-spacing: 0.2px;">TOTAL ALL TIME</div>
            </div>
        </div>

        <!-- Chart Container Full Width with Bottom-Right Toggles -->
        <div style="width: 100%; height: 320px; position: relative; border-top: 1px dashed #eee; border-bottom: 1px dashed #eee;">
            <canvas id="statsChart"></canvas>
            <!-- Chart Toggles Overlapping Bottom Right -->
            <div style="position: absolute; bottom: 12px; right: 12px; display: flex; gap: 6px; z-index: 10;">
                <div id="btnLineChart" class="stats-toggle-btn active" onclick="toggleChartType('line')" style="background: rgba(255,255,255,0.9); box-shadow: 0 2px 8px rgba(0,0,0,0.1); color: #666; border: none; border-radius: 8px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline></svg>
                </div>
                <div id="btnBarChart" class="stats-toggle-btn" onclick="toggleChartType('bar')" style="background: rgba(255,255,255,0.9); box-shadow: 0 2px 8px rgba(0,0,0,0.1); color: #666; border: none; border-radius: 8px; width: 36px; height: 36px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M18 20V10M12 20V4M6 20v-4"></path></svg>
                </div>
            </div>
        </div>

        <!-- Exercise Icon Bottom Bar (8 in a row) -->
        <div style="padding: 24px 12px; width: 100%; box-sizing: border-box;">
            <div id="statsExerciseFilter" style="display: flex; justify-content: space-between; align-items: center; width: 100%;">
                <!-- Icons injected via JS -->
            </div>
        </div>
    </div>'''

html = re.sub(r'    <!-- Stats View \(TradingView Style\) -->.*?    <!-- Floating Bottom Navigation -->', new_stats_view + '\n\n    <!-- Floating Bottom Navigation -->', html, flags=re.DOTALL)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
