import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add translation dictionary and language logic at the top, right after state variables
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
        'Slant Board Squat': 'Slant Board Squat'
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
        'Slant Board Squat': '斜板深蹲'
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
        el.textContent = t(key);
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
    renderCalendar();
    
    // Refresh Exercise Picker if open
    if (document.getElementById('exercisePickerModal').classList.contains('show')) {
        openExercisePicker();
    }
}

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('pushup_lang', lang);
    updateLanguageUI();
}
"""

js = js.replace('// --- App State ---', '// --- App State ---\n' + i18n_code)

# Now apply translations to dynamic JS rendering

# 1. Date rendering
js = js.replace(
    "document.getElementById('selectedDateDisplay').textContent = selectedDate.toLocaleDateString('en-US', dateOptions);",
    "document.getElementById('selectedDateDisplay').textContent = selectedDate.toLocaleDateString(currentLang === 'zh' ? 'zh-TW' : 'en-US', dateOptions);"
)
js = js.replace(
    "document.getElementById('selectedExerciseDate').textContent = selectedDate.toLocaleDateString('en-US', dateOptions);",
    "document.getElementById('selectedExerciseDate').textContent = selectedDate.toLocaleDateString(currentLang === 'zh' ? 'zh-TW' : 'en-US', dateOptions);"
)

# 2. Daily Logs Sets & Reps
js = js.replace(
    "</span> sets · <span",
    "</span> ${t('sets')} · <span"
)
js = js.replace(
    "</span> reps total</div>",
    "</span> ${t('reps')} ${t('total')}</div>"
)

# 3. Empty state
js = js.replace(
    "dailyLogList.innerHTML = '<div style=\"text-align: center; padding: 40px 20px; color: #999; font-size: 0.9rem;\">No logs today</div>';",
    "dailyLogList.innerHTML = `<div style=\"text-align: center; padding: 40px 20px; color: #999; font-size: 0.9rem;\">${t('no_logs')}</div>`;"
)

# 4. Exercise Names in daily logs
js = js.replace(
    '<span style="color: var(--text-primary); font-weight: 600; font-size: 1rem;">${entry.type}</span>',
    '<span style="color: var(--text-primary); font-weight: 600; font-size: 1rem;">${t(entry.type)}</span>'
)

# 5. Stats Header Title
js = js.replace(
    "document.getElementById('statsHeaderTitle').textContent = currentStatsExercise;",
    "document.getElementById('statsHeaderTitle').textContent = t(currentStatsExercise);"
)

# 6. Stats Today / This week
js = js.replace(
    "todayLabel.innerHTML = `+${todayTotal.toLocaleString()} today`;",
    "todayLabel.innerHTML = `+${todayTotal.toLocaleString()} ${t('today')}`;"
)
js = js.replace(
    "weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} +${weeklyTotal.toLocaleString()} this week`;",
    "weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${currentLang === 'zh' ? '天' : dayWord} +${weeklyTotal.toLocaleString()} ${t('this_week')}`;"
)

# 7. Exercise Picker
js = js.replace(
    "label.innerHTML = ex === 'Polyquin Step-down' ? 'Polyquin<br>Step-down' : ex;",
    "label.innerHTML = t(ex).replace(' ', '<br>'); // Simple wrap for long names if needed, but zh is short"
)

# 8. Add updateLanguageUI() to init()
js = js.replace(
    "renderCalendar();",
    "updateLanguageUI();\n    renderCalendar();"
)


with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
