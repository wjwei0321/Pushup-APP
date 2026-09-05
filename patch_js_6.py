import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add keys to EN
js = js.replace(
    "logged_success: 'Logged successfully!',",
    "logged_success: 'Logged!',\n        alert_select_exercise: 'Please select an exercise.',\n        alert_valid_reps: 'Please enter valid reps.',"
)

# Add keys to ZH
js = js.replace(
    "logged_success: '記錄成功！',",
    "logged_success: '已記錄！',\n        alert_select_exercise: '請選擇一個運動。',\n        alert_valid_reps: '請輸入有效的次數。',"
)

# Patch the usage
js = js.replace(
    "alert('Please select an exercise.')",
    "alert(t('alert_select_exercise'))"
)
js = js.replace(
    "alert('Please enter valid reps.')",
    "alert(t('alert_valid_reps'))"
)
js = js.replace(
    'showToast("Logged!");',
    'showToast(t("logged_success"));'
)
js = js.replace(
    "if (!msg) msg = t(\"logged_success\");",
    ""
)
js = js.replace(
    "function showToast(msg) {",
    "function showToast(msg = t('logged_success')) {"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
