// State
let trainingData = [];
let currentDate = new Date(); // Month currently viewed
let selectedDate = new Date(); // Date currently selected
let apiUrl = 'https://script.google.com/macros/s/AKfycbzULLYM8Qow0Ra3ZO3qv6l6aw7kticNlaI0sr3PAkqHDQdKY50e3v8GN5av14V8Q46n/exec';
let selectedExerciseForLog = null;
let activeFilters = []; // empty means "Show All"

// Icons Dictionary — Caly-style bold silhouette figures
const EXERCISES = {
    'Push-up': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="20" cy="8" r="2" fill="currentColor"/><path d="M3 17h2l3-2h7l3-4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="18" y1="11" x2="18" y2="15" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'Pull-up': '<svg width="100%" height="100%" viewBox="0 0 24 24"><line x1="4" y1="2" x2="20" y2="2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><circle cx="12" cy="6" r="2" fill="currentColor"/><path d="M8 2l2 4h4l2-4" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/><line x1="12" y1="8" x2="12" y2="15" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 15l-3 6M12 15l3 6" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
    'Lunge': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="13" cy="3" r="2" fill="currentColor"/><line x1="13" y1="5" x2="13" y2="11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M13 11l-6 5-2 0" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M13 11l3 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="7" y1="16" x2="5" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="16" y1="14" x2="16" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>',
    'Glute Band': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="10" cy="3" r="2" fill="currentColor"/><line x1="10" y1="5" x2="10" y2="11" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M10 11l-3 4v5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M10 11l5-2" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="7" y1="15" x2="7" y2="21" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M13 13l3 3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-dasharray="3 2" fill="none"/></svg>',
    'Polyquen Step-up': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="11" cy="2" r="2" fill="currentColor"/><line x1="11" y1="4" x2="11" y2="9" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M11 9l-3 4v1" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M11 9l2 2v3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><rect x="3" y="14" width="18" height="3" rx="1" fill="currentColor" opacity="0.3"/><rect x="3" y="18" width="18" height="3" rx="1" fill="currentColor" opacity="0.15"/></svg>',
    'Hack Squat': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="12" cy="3" r="2" fill="currentColor"/><line x1="9" y1="5" x2="15" y2="5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="12" y1="5" x2="12" y2="10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 10l-4 5v2l-1 4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M12 10l4 5v2l1 4" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/></svg>',
    'Romanian Deadlift': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="16" cy="4" r="2" fill="currentColor"/><path d="M16 6l-7 8" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M16 6l2 5" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><line x1="9" y1="14" x2="7" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="18" y1="11" x2="19" y2="20" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><line x1="5" y1="20" x2="21" y2="20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
    'Slant Board Squat': '<svg width="100%" height="100%" viewBox="0 0 24 24"><circle cx="12" cy="3" r="2" fill="currentColor"/><line x1="12" y1="5" x2="12" y2="10" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/><path d="M12 10l-3 4-1 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M12 10l3 4 1 3" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/><path d="M4 21l16-5v5z" fill="currentColor" opacity="0.25"/></svg>'
};

// DOM Elements
const calendarDaysEl = document.getElementById('calendarDays');
const currentMonthYearEl = document.getElementById('currentMonthYear');
const selectedDateDisplay = document.getElementById('selectedDateDisplay');
const dailyLogList = document.getElementById('dailyLogList');
const addWorkoutModal = document.getElementById('addWorkoutModal');
const settingsModal = document.getElementById('settingsModal');
const exerciseDropdown = document.getElementById('exerciseDropdown');
const filterModal = document.getElementById('filterModal');
const headerFilterBtn = document.getElementById('headerFilterBtn');

// Init
document.addEventListener('DOMContentLoaded', () => {
    initExerciseListGrid();
    initFilterModal();
    renderCalendar();
    fetchData();
    initPullToRefresh();
    initScrollNav();

    // Close modals when clicking outside (using direct listeners for mobile compatibility)
    document.querySelectorAll('.modal').forEach(modal => {
        const dismissHandler = (e) => {
            if (e.target === modal) {
                if (modal.id === 'addWorkoutModal') closeAddWorkoutModal();
                if (modal.id === 'filterModal') closeFilterModal();
                if (modal.id === 'settingsModal') {
                    modal.classList.remove('show');
                    setTimeout(() => modal.style.display = 'none', 300);
                }
            }
        };
        modal.addEventListener('mousedown', dismissHandler);
        modal.addEventListener('touchstart', dismissHandler, {passive: true});
        
        // Swipe down to dismiss
        const content = modal.querySelector('.modal-content');
        if (content) {
            let startY = 0;
            let currentY = 0;
            
            content.addEventListener('touchstart', (e) => {
                const scroller = e.target.closest('[style*="overflow-y"]');
                if (scroller && scroller.scrollTop > 0) return; // Don't drag if scrolling inner content
                startY = e.touches[0].clientY;
                currentY = 0;
                content.style.transition = 'none';
            }, {passive: true});
            
            content.addEventListener('touchmove', (e) => {
                if (startY === 0) return;
                const deltaY = e.touches[0].clientY - startY;
                if (deltaY > 0) {
                    if (e.cancelable) e.preventDefault();
                    currentY = deltaY;
                    content.style.transform = `translateY(${deltaY}px)`;
                }
            }, {passive: false});
            
            content.addEventListener('touchend', () => {
                if (startY === 0) return;
                content.style.transition = 'transform 0.3s ease-out';
                if (currentY > 100) {
                    // Dismiss by driving the sheet down
                    content.style.transform = 'translateY(100%)';
                    
                    if (modal.id === 'addWorkoutModal') closeAddWorkoutModal();
                    if (modal.id === 'filterModal') closeFilterModal();
                    if (modal.id === 'settingsModal') {
                        modal.classList.remove('show');
                        setTimeout(() => modal.style.display = 'none', 300);
                    }
                    setTimeout(() => { content.style.transform = ''; }, 300);
                } else {
                    // Snap back
                    content.style.transform = '';
                }
                startY = 0;
            });
        }
    });
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
    const homeView = document.getElementById('homeView');

    document.addEventListener('touchstart', e => {
        if (document.querySelector('.modal.show')) return;
        if (window.scrollY <= 0) {
            touchStartY = e.touches[0].clientY;
        }
    }, {passive: true});

    document.addEventListener('touchmove', e => {
        if (touchStartY === 0 || isRefreshing || document.querySelector('.modal.show')) return;
        const touchY = e.touches[0].clientY;
        const delta = touchY - touchStartY;
        
        // If we are at the top and pulling down
        if (delta > 0 && window.scrollY <= 0) {
            if (e.cancelable) {
                e.preventDefault(); // Stop native iOS rubber banding!
            }
            ptr.style.opacity = Math.min(delta / 100, 1);
            homeView.style.transform = `translateY(${Math.min(delta / 2, 80)}px)`;
            ptr.style.transform = `rotate(${delta}deg)`;
        }
    }, {passive: false});

    document.addEventListener('touchend', e => {
        if (touchStartY === 0 || isRefreshing) return;
        const touchY = e.changedTouches[0].clientY;
        const delta = touchY - touchStartY;
        
        if (delta > 100 && window.scrollY <= 0) {
            isRefreshing = true;
            ptr.classList.add('spinning');
            homeView.style.transform = `translateY(60px)`;
            
            fetchData().then(() => {
                isRefreshing = false;
                ptr.classList.remove('spinning');
                homeView.style.transform = `translateY(0)`;
                ptr.style.opacity = 0;
            });
        } else {
            homeView.style.transform = `translateY(0)`;
            ptr.style.opacity = 0;
        }
        touchStartY = 0;
    });
}

function initExerciseListGrid() {
    const grid = document.getElementById('exerciseListGrid');
    grid.innerHTML = '';
    Object.keys(EXERCISES).forEach(ex => {
        const btn = document.createElement('div');
        btn.style.cssText = 'border: 1.5px solid var(--text-primary); border-radius: 16px; padding: 20px; display: flex; align-items: center; gap: 20px; cursor: pointer; background: var(--card-bg); font-weight: 700; font-size: 1.2rem; transition: transform 0.1s;';
        btn.innerHTML = `<div style="width:32px; height:32px; display:flex; align-items:center; justify-content:center;">${EXERCISES[ex]}</div> <span>${ex}</span>`;
        btn.onclick = () => selectExercise(ex);
        btn.onmousedown = () => btn.style.transform = 'scale(0.97)';
        btn.onmouseup = () => btn.style.transform = 'scale(1)';
        btn.ontouchstart = () => btn.style.transform = 'scale(0.97)';
        btn.ontouchend = () => btn.style.transform = 'scale(1)';
        grid.appendChild(btn);
    });
}

// Filter Logic
function initFilterModal() {
    const list = document.getElementById('filterList');
    list.innerHTML = '';
    
    // Add "Show All"
    const allDiv = document.createElement('div');
    allDiv.className = 'filter-item selected';
    allDiv.id = 'filterItem_ALL';
    allDiv.innerHTML = `<span>Show All</span> <div class="filter-checkbox"></div>`;
    allDiv.onclick = () => toggleFilter('ALL');
    list.appendChild(allDiv);

    // Add Exercises
    Object.keys(EXERCISES).forEach(ex => {
        const exDiv = document.createElement('div');
        exDiv.className = 'filter-item';
        exDiv.id = `filterItem_${ex.replace(/\s+/g, '_')}`;
        exDiv.innerHTML = `
            <div style="display:flex; align-items:center; gap:12px;">
                <div style="width:24px; height:24px;">${EXERCISES[ex]}</div>
                <span>${ex}</span>
            </div>
            <div class="filter-checkbox"></div>
        `;
        exDiv.onclick = () => toggleFilter(ex);
        list.appendChild(exDiv);
    });
}

function openFilterModal() {
    filterModal.style.display = 'flex';
    setTimeout(() => filterModal.classList.add('show'), 10);
}

function closeFilterModal() {
    filterModal.classList.remove('show');
    setTimeout(() => filterModal.style.display = 'none', 300);
}

function toggleFilter(type) {
    if (type === 'ALL') {
        activeFilters = [];
    } else {
        if (activeFilters.includes(type)) {
            activeFilters = activeFilters.filter(f => f !== type);
        } else {
            activeFilters.push(type);
        }
    }
    
    // Update UI checkmarks
    document.getElementById('filterItem_ALL').classList.toggle('selected', activeFilters.length === 0);
    Object.keys(EXERCISES).forEach(ex => {
        const item = document.getElementById(`filterItem_${ex.replace(/\s+/g, '_')}`);
        if (item) {
            item.classList.toggle('selected', activeFilters.includes(ex));
        }
    });

    // Update Header Button
    if (activeFilters.length === 0) {
        headerFilterBtn.classList.remove('active');
        headerFilterBtn.innerHTML = 'A';
    } else if (activeFilters.length === 1) {
        headerFilterBtn.classList.add('active');
        headerFilterBtn.innerHTML = `<div style="width:20px;height:20px;display:flex;">${EXERCISES[activeFilters[0]]}</div>`;
    } else {
        headerFilterBtn.classList.add('active');
        headerFilterBtn.innerHTML = activeFilters.length;
    }

    renderCalendar();
    renderDailyLog();
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
    const today = new Date();
    for (let i = 1; i <= daysInMonth; i++) {
        const cell = document.createElement('div');
        cell.className = 'day-cell';
        
        const numSpan = document.createElement('span');
        numSpan.className = 'day-number';
        numSpan.textContent = i;
        
        if (year === today.getFullYear() && month === today.getMonth() && i === today.getDate()) {
            numSpan.classList.add('today');
        }
        cell.appendChild(numSpan);
        
        // Check if selected
        if (year === selectedDate.getFullYear() && month === selectedDate.getMonth() && i === selectedDate.getDate()) {
            cell.classList.add('selected');
        }
        
        // Check for data
        const dateStr = `${year}/${String(month+1).padStart(2, '0')}/${String(i).padStart(2, '0')}`;
        let dayData = trainingData.filter(d => d.dateStr === dateStr);
        
        if (activeFilters.length > 0) {
            dayData = dayData.filter(d => activeFilters.includes(d.type));
        }
        
        if (dayData.length > 0) {
            const container = document.createElement('div');
            container.className = 'day-icons-container';
            
            // Group by exercise type
            const exerciseSets = {};
            dayData.forEach(d => {
                if (!exerciseSets[d.type]) exerciseSets[d.type] = 0;
                exerciseSets[d.type] += d.sets.length;
            });

            const distinctCount = Object.keys(exerciseSets).length;
            Object.keys(exerciseSets).forEach(exType => {
                const sets = exerciseSets[exType];
                
                // Scale proportion according to quantity
                let size = 16 + (sets * 3); 
                if (size > 28) size = 28; // Max size to prevent overflow
                
                if (distinctCount > 2) size = Math.min(size, 16);
                else if (distinctCount > 1) size = Math.min(size, 20);
                
                const ind = document.createElement('div');
                ind.className = 'day-indicator';
                ind.style.width = `${size}px`;
                ind.style.height = `${size}px`;
                ind.innerHTML = EXERCISES[exType];
                container.appendChild(ind);
            });
            cell.appendChild(container);
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
    let dayData = trainingData.filter(d => d.dateStr === dateStr);
    
    if (activeFilters.length > 0) {
        dayData = dayData.filter(d => activeFilters.includes(d.type));
    }
    
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
                <div class="log-card-actions" style="position: absolute; top: 0; right: 0; height: 100%; display: flex; z-index: 1;">
                    <button class="edit-swipe-btn" onclick="enableEditMode(this, ${entry.rowIndex}, ${setIndex})" style="background: var(--text-secondary); color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button class="delete-swipe-btn" onclick="confirmDeleteSet(${entry.rowIndex}, ${setIndex})" style="background: #e74c3c; color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer; border-radius: 0 16px 16px 0;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                    </button>
                </div>
                <div class="log-card-content" style="position: relative; z-index: 2; background: white; padding: 20px; border-radius: 16px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 4px 15px rgba(0,0,0,0.03); transition: transform 0.2s ease-out; transform: translateX(0);">
                    <div class="log-card-left" style="display: flex; align-items: center; gap: 15px;">
                        <div class="log-icon">${iconSvg}</div>
                        <div class="log-details" style="display: flex; flex-direction: column;">
                            <span class="log-title" style="font-weight: 700; font-size: 1rem;">${entry.type}</span>
                            <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">Set ${setIndex + 1}</span>
                        </div>
                    </div>
                    <input type="number" class="inline-edit-input" data-row="${entry.rowIndex}" data-set="${setIndex}" value="${repCount}" readonly onblur="saveInlineEdit(this)" onkeydown="if(event.key==='Enter') this.blur();" style="font-size: 1.8rem; font-weight: 800; border: none; background: transparent; width: 70px; text-align: right; color: var(--text-primary); font-family: inherit; outline: none; padding: 0;">
                </div>
            `;
            
            initSwipeActions(card);
            
            dailyLogList.appendChild(card);
        });
    });
}

// Inline Edit & Swipe Logic
function initSwipeActions(card) {
    const content = card.querySelector('.log-card-content');
    let startX = 0;
    let currentX = 0;
    let isDragging = false;
    
    // Total width of actions on the right is 140px (70 + 70)
    const actionWidth = -140;

    content.addEventListener('touchstart', e => {
        if (e.target.tagName.toLowerCase() === 'input') return; // Don't drag if focusing input
        startX = e.touches[0].clientX;
        isDragging = true;
        content.style.transition = 'none';
    }, {passive: true});
    
    content.addEventListener('touchmove', e => {
        if (!isDragging) return;
        const x = e.touches[0].clientX;
        const diff = x - startX;
        
        // If swiping left, allow up to actionWidth, with some rubber-banding
        if (diff < 0) {
            currentX = Math.max(diff, actionWidth - 20);
        } else {
            // Swiping right (closing)
            currentX = Math.max(currentX + (x - startX), actionWidth);
            currentX = Math.min(currentX, 20); // Rubber band right
        }
        
        content.style.transform = `translateX(${currentX}px)`;
    }, {passive: true});
    
    content.addEventListener('touchend', () => {
        if (!isDragging) return;
        isDragging = false;
        content.style.transition = 'transform 0.2s ease-out';
        
        // Snap open or close
        if (currentX < actionWidth / 2) {
            currentX = actionWidth;
        } else {
            currentX = 0;
        }
        content.style.transform = `translateX(${currentX}px)`;
    });
}

function enableEditMode(btn, rowIndex, setIndex) {
    // Snap card back
    const card = btn.closest('.log-card');
    const content = card.querySelector('.log-card-content');
    content.style.transform = 'translateX(0)';
    
    // Focus input
    const input = content.querySelector('.inline-edit-input');
    input.removeAttribute('readonly');
    input.style.borderBottom = '2px solid var(--accent-color)';
    input.style.borderRadius = '0';
    input.focus();
    
    // Move cursor to end
    const val = input.value;
    input.value = '';
    input.value = val;
}

function saveInlineEdit(input) {
    input.setAttribute('readonly', 'true');
    input.style.borderBottom = 'none';
    
    const rowIndex = parseInt(input.getAttribute('data-row'));
    const setIndex = parseInt(input.getAttribute('data-set'));
    const newVal = parseInt(input.value);
    
    if (isNaN(newVal) || newVal <= 0) {
        showToast('Invalid number. Reverting...');
        renderDailyLog(); // Revert UI to old state
        return;
    }
    
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    // Only update if changed
    if (entry.sets[setIndex] !== newVal) {
        entry.sets[setIndex] = newVal;
        updateSetOnBackend(entry);
    }
}

function confirmDeleteSet(rowIndex, setIndex) {
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    if (confirm(`Delete Set ${setIndex + 1}?`)) {
        entry.sets.splice(setIndex, 1);
        updateSetOnBackend(entry);
    } else {
        // Snap back
        renderDailyLog();
    }
}

async function updateSetOnBackend(entry) {
    // Optimistic UI Update
    renderDailyLog();
    showToast('Updating...');
    
    // If no sets left, delete the entire row
    const payload = {
        action: entry.sets.length === 0 ? 'delete' : 'edit',
        rowIndex: entry.rowIndex - 2, // Backend expects 0-index based on row 2
        reps: entry.sets
    };
    
    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        
        if (result.status === 'success') {
            showToast('Updated successfully!');
            fetchData();
        } else {
            showToast('Error: ' + result.message);
        }
    } catch (e) {
        console.error(e);
        showToast('Error updating record');
    }
}

// Modal Logic
function openAddWorkoutModal() {
    selectedExerciseForLog = null;
    document.getElementById('stepSelectExercise').style.display = 'flex';
    document.getElementById('stepInputReps').style.display = 'none';
    document.getElementById('workoutRepsDisplay').textContent = '0';
    
    addWorkoutModal.style.display = 'flex';
    setTimeout(() => addWorkoutModal.classList.add('show'), 10);
}

function closeAddWorkoutModal() {
    addWorkoutModal.classList.remove('show');
    setTimeout(() => addWorkoutModal.style.display = 'none', 300);
}

function selectExercise(type) {
    selectedExerciseForLog = type;
    document.getElementById('selectedExerciseTitle').textContent = type;
    
    const dateOptions = { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric' };
    document.getElementById('selectedExerciseDate').textContent = selectedDate.toLocaleDateString('en-US', dateOptions);
    
    document.getElementById('selectedExerciseIconLarge').innerHTML = `<div style="width: 140px; height: 140px; background: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; padding: 28px; box-sizing: border-box;">${EXERCISES[type]}</div>`;
    
    updateModalStats();

    document.getElementById('stepSelectExercise').style.display = 'none';
    document.getElementById('stepInputReps').style.display = 'flex';
}

function addReps(amount) {
    const display = document.getElementById('workoutRepsDisplay');
    let current = parseInt(display.textContent) || 0;
    display.textContent = current + amount;
}

function clearReps() {
    document.getElementById('workoutRepsDisplay').textContent = '0';
}

function backToExerciseSelection() {
    document.getElementById('stepInputReps').style.display = 'none';
    document.getElementById('stepSelectExercise').style.display = 'flex';
}

function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const dayRow = trainingData.find(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = 0;
    let totalReps = 0;
    if (dayRow) {
        sets = dayRow.sets.length;
        totalReps = dayRow.sets.reduce((sum, val) => sum + val, 0);
    }
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}

async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
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
    
    // Update UI and keep modal open for continuous input
    clearReps();
    updateModalStats();
    renderCalendar();
    renderDailyLog();
    showToast("Logged!");
    
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
