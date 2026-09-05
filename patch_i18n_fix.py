import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

i18n_code = """
// --- i18n ---
const I18N = {
    en: {
        strive_to_evolve: 'STRIVE TO EVOLVE',
        wd_0: 'S', wd_1: 'M', wd_2: 'T', wd_3: 'W', wd_4: 'T', wd_5: 'F', wd_6: 'S',
        select_exercise: 'Select Exercise',
        input_reps: 'Input Reps',
        manual_input: 'Manual Input',
        log_workout: 'Log Workout',
        edit_log: 'Edit Log',
        update: 'Update',
        profile: 'Profile',
        email: 'Email',
        enter_email: 'Enter your email',
        save_sync: 'Save & Sync',
        sets: 'sets',
        reps: 'reps',
        total: 'total',
        today: 'today',
        this_week: 'this week',
        no_logs: 'No logs today',
        'Push-up': 'Push-up',
        'Pull-up': 'Pull-up',
        'Squat': 'Squat',
        'Dip': 'Dip',
        'Core': 'Core',
        'Pistol Squat': 'Pistol Squat',
        'Muscle-up': 'Muscle-up',
        'Polyquin Step-down': 'Polyquin Step-down',
        'Glutes Medius Slide Plank': 'Glutes Medius Slide Plank',
        'Slant Board Squat': 'Slant Board Squat',
        sets_upper: 'SETS',
        total_upper: 'TOTAL',
        not_logged_in: 'Not logged in',
        select_exercises: 'Select Exercises',
        clear_btn: 'C',
        api_url: 'API URL',
        logged_success: 'Logged!',
        sync_failed: 'Sync Failed',
        syncing: 'Syncing...',
        alert_select_exercise: 'Please select an exercise.',
        alert_valid_reps: 'Please enter valid reps.'
    },
    zh: {
        strive_to_evolve: 'STRIVE TO EVOLVE',
        wd_0: '日', wd_1: '一', wd_2: '二', wd_3: '三', wd_4: '四', wd_5: '五', wd_6: '六',
        select_exercise: '選擇運動',
        input_reps: '輸入次數',
        manual_input: '手動輸入',
        log_workout: '記錄運動',
        edit_log: '編輯紀錄',
        update: '更新',
        profile: '個人設定',
        email: '電子郵件',
        enter_email: '輸入電子郵件',
        save_sync: '儲存並同步',
        sets: '組',
        reps: '下',
        total: '總計',
        today: '今日',
        this_week: '本週',
        no_logs: '今日無紀錄',
        'Push-up': '伏地挺身',
        'Pull-up': '單槓',
        'Squat': '深蹲',
        'Dip': '雙槓撐體',
        'Core': '核心',
        'Pistol Squat': '單腳深蹲',
        'Muscle-up': '暴力上槓',
        'Polyquin Step-down': '階梯深蹲',
        'Glutes Medius Slide Plank': '側平板滑行',
        'Slant Board Squat': '斜板深蹲',
        sets_upper: '組數',
        total_upper: '總次數',
        not_logged_in: '未登入',
        select_exercises: '選擇運動',
        clear_btn: '清除',
        api_url: 'API 網址',
        logged_success: '已記錄！',
        sync_failed: '同步失敗',
        syncing: '同步中...',
        alert_select_exercise: '請選擇一個運動。',
        alert_valid_reps: '請輸入有效的次數。'
    }
};

let currentLang = localStorage.getItem('pushup_lang') || 'en';

function t(key) {
    if (!I18N[currentLang]) return key;
    return I18N[currentLang][key] || key;
}

function updateLanguageUI() {
    // Update data-i18n
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        el.innerHTML = t(key); // Changed to innerHTML to support <br> or other HTML if needed
    });
    
    // Update placeholders
    document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        el.placeholder = t(key);
    });
    
    // Update toggle buttons
    const btnEN = document.getElementById('btnLangEN');
    const btnZH = document.getElementById('btnLangZH');
    if (btnEN && btnZH) {
        if (currentLang === 'en') {
            btnEN.style.background = 'var(--accent-color)';
            btnEN.style.color = 'white';
            btnZH.style.background = 'transparent';
            btnZH.style.color = 'var(--text-secondary)';
        } else {
            btnZH.style.background = 'var(--accent-color)';
            btnZH.style.color = 'white';
            btnEN.style.background = 'transparent';
            btnEN.style.color = 'var(--text-secondary)';
        }
    }
    
    // Re-render JS dynamic text
    if (document.getElementById('statsView').style.display === 'block') {
        renderStats();
    }
}

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('pushup_lang', lang);
    updateLanguageUI();
    renderCalendar();
    renderDailyLog();
    
    // Refresh Exercise Picker if open
    if (document.getElementById('exercisePickerModal').classList.contains('show')) {
        openExercisePicker();
    }
}
"""

# Insert i18n_code right after the first line (const EXERCISES = {...) 
# Wait, let's insert it before `document.addEventListener('DOMContentLoaded', () => {`
idx = js.find("document.addEventListener('DOMContentLoaded'")
js = js[:idx] + i18n_code + "\n" + js[idx:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
