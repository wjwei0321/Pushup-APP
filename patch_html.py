import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Add data-i18n attributes to static text in index.html

# 1. Title
html = html.replace('>STRIVE TO EVOLVE<', ' data-i18n="strive_to_evolve">STRIVE TO EVOLVE<')

# 2. Weekdays
weekdays = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
for i, d in enumerate(weekdays):
    html = html.replace(f'<div class="weekday">{d}</div>', f'<div class="weekday" data-i18n="wd_{i}">{d}</div>', 1)

# 3. Add Workout Modal Header
html = html.replace('<h3 style="margin: 0; font-weight: 700;">Select Exercise</h3>', '<h3 style="margin: 0; font-weight: 700;" data-i18n="select_exercise">Select Exercise</h3>')
html = html.replace('<h3 id="stepInputTitle" style="margin: 0; font-weight: 700;">Input Reps</h3>', '<h3 id="stepInputTitle" style="margin: 0; font-weight: 700;" data-i18n="input_reps">Input Reps</h3>')

# 4. Manual Input Placeholder
html = html.replace('placeholder="Manual Input"', 'placeholder="Manual Input" data-i18n-placeholder="manual_input"')

# 5. Log Workout Button
html = html.replace('>Log Workout<', ' data-i18n="log_workout">Log Workout<')

# 6. Edit Modal
html = html.replace('<h3 style="margin: 0; font-weight: 700;">Edit Log</h3>', '<h3 style="margin: 0; font-weight: 700;" data-i18n="edit_log">Edit Log</h3>')
html = html.replace('>Update<', ' data-i18n="update">Update<')

# 7. Profile Modal
html = html.replace('>Profile<', ' data-i18n="profile">Profile<')
html = html.replace('>Email</label>', ' data-i18n="email">Email</label>')
html = html.replace('placeholder="Enter your email"', 'placeholder="Enter your email" data-i18n-placeholder="enter_email"')
html = html.replace('>Save & Sync<', ' data-i18n="save_sync">Save & Sync<')

# Insert Language Toggle in Profile Modal
toggle_html = """
            <div class="lang-toggle" style="display: flex; background: var(--bg-color); border-radius: 8px; margin-bottom: 20px; padding: 4px;">
                <div id="btnLangEN" onclick="setLanguage('en')" style="flex: 1; text-align: center; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: 0.2s; background: var(--accent-color); color: white;">EN</div>
                <div id="btnLangZH" onclick="setLanguage('zh')" style="flex: 1; text-align: center; padding: 8px; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: 0.2s; color: var(--text-secondary);">中文</div>
            </div>
"""
html = html.replace('<div id="apiUrlContainer"', toggle_html + '            <div id="apiUrlContainer"')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
