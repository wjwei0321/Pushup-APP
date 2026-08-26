// State
let trainingData = [];
let currentDate = new Date(); // Month currently viewed
let selectedDate = new Date(); // Date currently selected
let apiUrl = 'https://script.google.com/macros/s/AKfycbzULLYM8Qow0Ra3ZO3qv6l6aw7kticNlaI0sr3PAkqHDQdKY50e3v8GN5av14V8Q46n/exec';
let selectedExerciseForLog = null;

// Icons Dictionary — Clay-style humanoid figures
const EXERCISES = {
    'Push-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="19" cy="9" r="2"/><line x1="4" y1="17" x2="7" y2="17"/><path d="M7 17l4-2 4 0 2-3"/><line x1="15" y1="12" x2="17" y2="14"/></svg>',
    'Pull-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="3" x2="20" y2="3"/><circle cx="12" cy="7" r="2"/><path d="M9 3l1 4m5-4l-1 4"/><line x1="12" y1="9" x2="12" y2="15"/><line x1="12" y1="15" x2="9" y2="21"/><line x1="12" y1="15" x2="15" y2="21"/></svg>',
    'Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M12 6v4"/><path d="M12 10l-4 4v3"/><path d="M12 10l4 4v3"/><path d="M8 14h8"/><line x1="8" y1="17" x2="7" y2="21"/><line x1="16" y1="17" x2="17" y2="21"/></svg>',
    'Lunge': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="3" r="2"/><path d="M12 5v5"/><path d="M12 10l-5 5-1 5"/><path d="M12 10l4 3 2 1"/><line x1="7" y1="15" x2="5" y2="15"/><line x1="16" y1="13" x2="16" y2="20"/></svg>',
    'Plank': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="19" cy="10" r="2"/><line x1="17" y1="11" x2="5" y2="14"/><line x1="5" y1="14" x2="5" y2="18"/><line x1="17" y1="11" x2="17" y2="15"/></svg>',
    'Glute Band': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="10" cy="4" r="2"/><path d="M10 6v4"/><path d="M10 10l-3 5v5"/><path d="M10 10l3 2 4-1"/><line x1="7" y1="15" x2="7" y2="20"/><path d="M13 12l0 4" stroke-dasharray="2 2"/></svg>',
    'Polyquen Step-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="3" r="2"/><path d="M12 5v4"/><path d="M12 9l-3 4v3"/><path d="M12 9l3 1v3h-3"/><rect x="4" y="17" width="16" height="4" rx="1"/><rect x="8" y="13" width="8" height="4" rx="1"/></svg>',
    'Hack Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M12 6v3"/><path d="M12 9l-4 5v3"/><path d="M12 9l4 5v3"/><line x1="8" y1="17" x2="7" y2="21"/><line x1="16" y1="17" x2="17" y2="21"/><line x1="9" y1="6" x2="15" y2="6"/></svg>',
    'Romanian Deadlift': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="14" cy="5" r="2"/><path d="M14 7l-5 7"/><path d="M14 7l2 4"/><line x1="9" y1="14" x2="7" y2="19"/><line x1="16" y1="11" x2="17" y2="19"/><line x1="6" y1="19" x2="18" y2="19"/></svg>',
    'Slant Board Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="4" r="2"/><path d="M12 6v4"/><path d="M12 10l-3 4"/><path d="M12 10l3 4"/><line x1="9" y1="14" x2="8" y2="18"/><line x1="15" y1="14" x2="16" y2="18"/><path d="M4 21l16-5v5z"/></svg>'
};

// DOM Elements
const calendarDaysEl = document.getElementById('calendarDays');
const currentMonthYearEl = document.getElementById('currentMonthYear');
const selectedDateDisplay = document.getElementById('selectedDateDisplay');
const dailyLogList = document.getElementById('dailyLogList');
const addWorkoutModal = document.getElementById('addWorkoutModal');
const settingsModal = document.getElementById('settingsModal');
const exerciseDropdown = document.getElementById('exerciseDropdown');

// Init
document.addEventListener('DOMContentLoaded', () => {
    initExerciseDropdown();
    renderCalendar();
    fetchData();
    initPullToRefresh();
    initScrollNav();
});

// Scroll to hide/show navigation
function initScrollNav() {
    let lastScrollY = window.scrollY;
    const nav = document.querySelector('.floating-nav');
    
    window.addEventListener('scroll', () => {
        const currentScrollY = window.scrollY;
        
        // Hide when scrolling down, show when scrolling up
        if (currentScrollY > lastScrollY && currentScrollY > 50) {
            nav.classList.add('hidden');
        } else {
            nav.classList.remove('hidden');
        }
        
        lastScrollY = currentScrollY;
    }, { passive: true });
}

// Pull to refresh logic
function initPullToRefresh() {
    let touchStartY = 0;
    let isRefreshing = false;
    const ptr = document.getElementById('ptrIndicator');

    document.addEventListener('touchstart', e => {
        if (window.scrollY <= 0) {
            touchStartY = e.touches[0].clientY;
        }
    }, {passive: true});

    document.addEventListener('touchmove', e => {
        if (touchStartY === 0 || isRefreshing) return;
        const touchY = e.touches[0].clientY;
        const delta = touchY - touchStartY;
        
        // If we are at the top and pulling down
        if (delta > 0 && window.scrollY <= 0) {
            if (e.cancelable) {
                e.preventDefault(); // Stop native iOS rubber banding!
            }
            ptr.style.opacity = Math.min(delta / 100, 1);
            ptr.style.transform = `translateY(${Math.min(delta / 2, 120)}px) rotate(${delta}deg)`;
        }
    }, {passive: false});

    document.addEventListener('touchend', e => {
        if (touchStartY === 0 || isRefreshing) return;
        const touchY = e.changedTouches[0].clientY;
        const delta = touchY - touchStartY;
        
        if (delta > 100 && window.scrollY <= 0) {
            isRefreshing = true;
            ptr.classList.add('spinning');
            ptr.style.transform = `translateY(120px)`;
            
            fetchData().then(() => {
                isRefreshing = false;
                ptr.classList.remove('spinning');
                ptr.style.transform = `translateY(0)`;
                ptr.style.opacity = 0;
                showToast("Updated!");
            });
        } else {
            ptr.style.transform = `translateY(0)`;
            ptr.style.opacity = 0;
        }
        touchStartY = 0;
    });
}

function initExerciseDropdown() {
    exerciseDropdown.innerHTML = '';
    Object.keys(EXERCISES).forEach(ex => {
        const div = document.createElement('div');
        div.className = 'dropdown-item';
        div.innerHTML = `${EXERCISES[ex]} <span>${ex}</span>`;
        div.onclick = () => selectExercise(ex);
        exerciseDropdown.appendChild(div);
    });
}

// Data Fetching
async function fetchData() {
    try {
        const res = await fetch(`${apiUrl}?action=get`);
        const json = await res.json();
        if (json.status === 'success') {
            // Data is [Date, Type, Set1, Set2, Set3, Set4, Set5, Set6]
            trainingData = json.data.filter(row => row[0]).map((row, index) => {
                const dateObj = new Date(row[0]);
                const dateStr = `${dateObj.getFullYear()}/${String(dateObj.getMonth()+1).padStart(2, '0')}/${String(dateObj.getDate()).padStart(2, '0')}`;
                
                // Parse sets
                let sets = [];
                for(let i = 2; i <= 7; i++) {
                    if (row[i] && !isNaN(parseInt(row[i]))) {
                        sets.push(parseInt(row[i]));
                    }
                }
                
                return {
                    rowIndex: index + 2, // Sheet row
                    dateStr: dateStr,
                    type: row[1],
                    sets: sets
                };
            });

            // 自動跳轉到「最近一筆紀錄」的月份與日期
            if (trainingData.length > 0) {
                const latestRecord = trainingData[trainingData.length - 1];
                const latestDateObj = new Date(latestRecord.dateStr);
                
                // 設定日曆當前顯示月份
                currentDate = new Date(latestDateObj.getFullYear(), latestDateObj.getMonth(), 1);
                // 設定當前選中日期
                selectedDate = new Date(latestDateObj.getFullYear(), latestDateObj.getMonth(), latestDateObj.getDate());
            }

            renderCalendar(); // Re-render to show indicators
            renderDailyLog(); // Re-render list
        }
    } catch (e) {
        console.error(e);
    }
}

// Calendar Logic
const MONTH_NAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];

function renderCalendar() {
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    currentMonthYearEl.textContent = `${MONTH_NAMES[month]} ${year}`;
    
    calendarDaysEl.innerHTML = '';
    
    const firstDay = new Date(year, month, 1).getDay();
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    
    // Empty cells before month
    for (let i = 0; i < firstDay; i++) {
        const cell = document.createElement('div');
        cell.className = 'day-cell empty';
        calendarDaysEl.appendChild(cell);
    }
    
    // Days
    for (let i = 1; i <= daysInMonth; i++) {
        const cell = document.createElement('div');
        cell.className = 'day-cell';
        cell.textContent = i;
        
        // Check if selected
        if (year === selectedDate.getFullYear() && month === selectedDate.getMonth() && i === selectedDate.getDate()) {
            cell.classList.add('selected');
        }
        
        // Check for data
        const dateStr = `${year}/${String(month+1).padStart(2, '0')}/${String(i).padStart(2, '0')}`;
        const dayData = trainingData.filter(d => d.dateStr === dateStr);
        let totalSetsToday = dayData.reduce((sum, d) => sum + d.sets.length, 0);
        
        if (totalSetsToday > 0) {
            const ind = document.createElement('div');
            ind.className = 'day-indicator';
            ind.innerHTML = EXERCISES[dayData[0].type] || EXERCISES['Push-up']; // Use first exercise icon
            
            if (totalSetsToday > 1) {
                const badge = document.createElement('div');
                badge.className = 'day-indicator-badge';
                badge.textContent = totalSetsToday;
                ind.appendChild(badge);
            }
            cell.appendChild(ind);
        }
        
        cell.onclick = () => {
            selectedDate = new Date(year, month, i);
            renderCalendar();
            renderDailyLog();
        };
        
        calendarDaysEl.appendChild(cell);
    }
}

function prevMonth() {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
}
function nextMonth() {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
}

// Daily Log Logic
function renderDailyLog() {
    const month = MONTH_NAMES[selectedDate.getMonth()].substring(0, 3);
    selectedDateDisplay.textContent = `${month} ${selectedDate.getDate()}`;
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const dayData = trainingData.filter(d => d.dateStr === dateStr);
    
    dailyLogList.innerHTML = '';
    
    if (dayData.length === 0) {
        dailyLogList.innerHTML = '<div style="text-align:center; padding: 20px; color: #aaa;">No workouts logged today.</div>';
        return;
    }
    
    dayData.forEach(entry => {
        entry.sets.forEach((repCount, setIndex) => {
            const card = document.createElement('div');
            card.className = 'log-card';
            
            const iconSvg = EXERCISES[entry.type] || EXERCISES['Push-up'];
            
            card.innerHTML = `
                <div class="log-card-left">
                    <div class="log-icon">${iconSvg}</div>
                    <div class="log-details">
                        <span class="log-title">${entry.type}</span>
                        <span class="log-time">Set ${setIndex + 1}</span>
                    </div>
                </div>
                <div class="log-reps">${repCount}</div>
            `;
            dailyLogList.appendChild(card);
        });
    });
}

// Modal Logic
function openAddWorkoutModal() {
    selectedExerciseForLog = null;
    document.getElementById('selectedExerciseText').textContent = 'Select exercise';
    document.getElementById('workoutRepsInput').value = '';
    document.getElementById('repsSection').style.display = 'none';
    
    addWorkoutModal.style.display = 'flex';
    setTimeout(() => addWorkoutModal.classList.add('show'), 10);
}

function closeAddWorkoutModal() {
    addWorkoutModal.classList.remove('show');
    setTimeout(() => addWorkoutModal.style.display = 'none', 300);
}

function toggleDropdown() {
    exerciseDropdown.classList.toggle('show');
}

function selectExercise(type) {
    selectedExerciseForLog = type;
    document.getElementById('selectedExerciseText').innerHTML = `<div style="display:flex; align-items:center; gap:8px;">${EXERCISES[type]} <span>${type}</span></div>`;
    exerciseDropdown.classList.remove('show');
    document.getElementById('repsSection').style.display = 'block';
    document.getElementById('workoutRepsInput').focus();
}

async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsInput').value;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    
    const payload = {
        action: 'log',
        date: dateStr,
        type: selectedExerciseForLog,
        exerciseType: selectedExerciseForLog,
        count: parseInt(reps)
    };
    
    // Optimistic UI Update
    let dayRow = trainingData.find(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    if (dayRow) {
        if(dayRow.sets.length >= 6) {
            alert('Max 6 sets allowed per day per exercise.');
            return;
        }
        dayRow.sets.push(parseInt(reps));
    } else {
        trainingData.push({
            rowIndex: -1,
            dateStr: dateStr,
            type: selectedExerciseForLog,
            sets: [parseInt(reps)]
        });
    }
    
    closeAddWorkoutModal();
    renderCalendar();
    renderDailyLog();
    showToast();
    
    try {
        await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        fetchData(); // Sync exact state
    } catch (e) {
        console.error(e);
    }
}

// Settings
function saveSettings() {
    const val = document.getElementById('apiUrl').value.trim();
    if (val) {
        apiUrl = val;
        localStorage.setItem('pushup_apiUrl', apiUrl);
        settingsModal.classList.remove('show');
        setTimeout(() => settingsModal.style.display = 'none', 300);
        fetchData();
    }
}

// Utils
function switchView(view) {
    // Only one view in this scope, prepared for future Stats page.
}

function showToast(msg = "Logged successfully!") {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}
