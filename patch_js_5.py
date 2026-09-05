import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add new keys to I18N en
js = js.replace(
    "'Slant Board Squat': 'Slant Board Squat'",
    "'Slant Board Squat': 'Slant Board Squat',\n        sets_upper: 'SETS',\n        total_upper: 'TOTAL',\n        not_logged_in: 'Not logged in',\n        select_exercises: 'Select Exercises',\n        clear_btn: 'C',\n        api_url: 'API URL',\n        logged_success: 'Logged successfully!',\n        sync_failed: 'Sync Failed',\n        syncing: 'Syncing...'"
)

# Add new keys to I18N zh
js = js.replace(
    "'Slant Board Squat': '斜板深蹲'",
    "'Slant Board Squat': '斜板深蹲',\n        sets_upper: '組數',\n        total_upper: '總次數',\n        not_logged_in: '未登入',\n        select_exercises: '選擇運動',\n        clear_btn: '清除',\n        api_url: 'API 網址',\n        logged_success: '記錄成功！',\n        sync_failed: '同步失敗',\n        syncing: '同步中...'"
)

# Patch showToast usages
js = js.replace(
    'function showToast(msg = "Logged successfully!") {',
    'function showToast(msg) {\n    if (!msg) msg = t("logged_success");'
)

# Patch initial userEmail rendering in init()
js = js.replace(
    "document.getElementById('currentUserDisplay').textContent = userEmail || 'Not logged in';",
    "document.getElementById('currentUserDisplay').textContent = userEmail || t('not_logged_in');"
)

# Patch fetchData texts
js = js.replace("showToast('Sync Failed');", "showToast(t('sync_failed'));")
js = js.replace("document.getElementById('currentUserDisplay').textContent = 'Syncing...';", "document.getElementById('currentUserDisplay').textContent = t('syncing');")
js = js.replace("document.getElementById('currentUserDisplay').textContent = userEmail || 'Not logged in';", "document.getElementById('currentUserDisplay').textContent = userEmail || t('not_logged_in');")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
