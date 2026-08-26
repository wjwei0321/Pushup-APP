// State
let trainingData = [];
let currentDate = new Date(); // Month currently viewed
let selectedDate = new Date(); // Date currently selected
let apiUrl = 'https://script.google.com/macros/s/AKfycbwfobM0NgTTxeaenrd7FWY7z4OmX22QvNbkEjMUxBxlxBdAXPSmoY-ZqnSFM1eTnms/exec';
let selectedExerciseForLog = null;

// Icons Dictionary
const EXERCISES = {
    'Push-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 14l4-4 4 4 4-4 4 4" /></svg>',
    'Pull-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 5h20M12 5v14M8 10h8" /></svg>',
    'Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm-3 6v12h2v-6h2v6h2V8H9z" /></svg>',
    'Lunge': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 4a2 2 0 1 0 0 4 2 2 0 0 0 0-4zM6 20v-6l4-4 2 4 4 6h3" /></svg>',
    'Plank': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" y1="18" x2="20" y2="18"></line><path d="M6 14l4-4 6 0 4 4"></path></svg>',
    'Glute Band': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="12" rx="10" ry="4"></ellipse></svg>',
    'Polyquen Step-up': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h6v-6h6v-6h4"></path></svg>',
    'Hack Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="4" y="4" width="16" height="16" rx="2"></rect><line x1="8" y1="12" x2="16" y2="12"></line></svg>',
    'Romanian Deadlift': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 18h20M12 18v-8M8 10h8"></path></svg>',
    'Slant Board Squat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="2 20 22 20 22 14 2 20"></polygon></svg>'
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
});

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
            trainingData = json.data.map((row, index) => {
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

function showToast() {
    const t = document.getElementById('toast');
    t.classList.add('show');
    setTimeout(() => t.classList.remove('show'), 3000);
}
