// State
let trainingData = [];
let currentDate = new Date(); // Month currently viewed
let selectedDate = new Date(); // Date currently selected
let apiUrl = 'https://script.google.com/macros/s/AKfycbzULLYM8Qow0Ra3ZO3qv6l6aw7kticNlaI0sr3PAkqHDQdKY50e3v8GN5av14V8Q46n/exec';
let selectedExerciseForLog = null;

// Icons Dictionary — Caly-style bold silhouette figures
const EXERCISES = {
    'Push-up': '<svg viewBox="0 0 24 24"><circle cx="20" cy="8" r="2" fill="currentColor"/><path d="M3 17h2l3-2h7l3-4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="18" y1="11" x2="18" y2="15" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'Pull-up': '<svg viewBox="0 0 24 24"><line x1="4" y1="2" x2="20" y2="2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><circle cx="12" cy="6" r="2" fill="currentColor"/><path d="M8 2l2 4h4l2-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/><line x1="12" y1="8" x2="12" y2="15" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 15l-3 6M12 15l3 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
    'Squat': '<svg viewBox="0 0 24 24"><circle cx="12" cy="3" r="2" fill="currentColor"/><path d="M10 7l-2 2v3h8v-3l-2-2" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M8 12l-1 5 2 0 2-3h2l2 3h2l-1-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/><path d="M9 17l-2 4M15 17l2 4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
    'Lunge': '<svg viewBox="0 0 24 24"><circle cx="13" cy="3" r="2" fill="currentColor"/><line x1="13" y1="5" x2="13" y2="11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M13 11l-6 5-2 0" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M13 11l3 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="7" y1="16" x2="5" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="16" y1="14" x2="16" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'Plank': '<svg viewBox="0 0 24 24"><circle cx="20" cy="9" r="2" fill="currentColor"/><path d="M4 16l14-4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="4" y1="16" x2="4" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="18" y1="12" x2="19" y2="16" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'Glute Band': '<svg viewBox="0 0 24 24"><circle cx="10" cy="3" r="2" fill="currentColor"/><line x1="10" y1="5" x2="10" y2="11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M10 11l-3 4v5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M10 11l5-2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="7" y1="15" x2="7" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M13 13l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-dasharray="3 2" fill="none"/></svg>',
    'Polyquen Step-up': '<svg viewBox="0 0 24 24"><circle cx="11" cy="2" r="2" fill="currentColor"/><line x1="11" y1="4" x2="11" y2="9" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M11 9l-3 4v1" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M11 9l2 2v3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><rect x="3" y="14" width="18" height="3" rx="1" fill="currentColor" opacity="0.3"/><rect x="3" y="18" width="18" height="3" rx="1" fill="currentColor" opacity="0.15"/></svg>',
    'Hack Squat': '<svg viewBox="0 0 24 24"><circle cx="12" cy="3" r="2" fill="currentColor"/><line x1="9" y1="5" x2="15" y2="5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="12" y1="5" x2="12" y2="10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 10l-4 5v2l-1 4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M12 10l4 5v2l1 4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
    'Romanian Deadlift': '<svg viewBox="0 0 24 24"><circle cx="16" cy="4" r="2" fill="currentColor"/><path d="M16 6l-7 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M16 6l2 5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="9" y1="14" x2="7" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="18" y1="11" x2="19" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="5" y1="20" x2="21" y2="20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    'Slant Board Squat': '<svg viewBox="0 0 24 24"><circle cx="12" cy="3" r="2" fill="currentColor"/><line x1="12" y1="5" x2="12" y2="10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 10l-3 4-1 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M12 10l3 4 1 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M4 21l16-5v5z" fill="currentColor" opacity="0.25"/></svg>'
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
        // 加入時間戳記避免瀏覽器快取 (Cache-busting)
        const timestamp = new Date().getTime();
        const res = await fetch(`${apiUrl}?action=get&t=${timestamp}`);
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
