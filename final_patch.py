import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix submitWorkout
js = re.sub(
    r'async function submitWorkout\(\) \{[\s\S]*?hideSplashScreen\(\);\n    \}\n\}',
    """async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const now = new Date();
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
    
    const payload = {
        action: 'add',
        email: userEmail,
        date: dateStr,
        type: selectedExerciseForLog,
        count: parseInt(reps),
        time: timeStr
    };
    
    // Optimistic UI Update
    trainingData.push({
        rowIndex: 999999 + Math.random(),
        dateStr: dateStr,
        type: selectedExerciseForLog,
        reps: parseInt(reps),
        time: timeStr
    });
    
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
        fetchData();
    } catch (e) {
        console.error(e);
        hideSplashScreen();
    }
}""",
    js
)

# Fix updateModalStats
js = re.sub(
    r'function updateModalStats\(\) \{[\s\S]*?document\.getElementById\(\'modalTotalRepsToday\'\)\.textContent = totalReps;\n\}',
    """function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const dayRows = trainingData.filter(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = dayRows.length;
    let totalReps = dayRows.reduce((sum, val) => sum + (val.reps || 0), 0);
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}""",
    js
)

# Fix saveInlineEdit
js = re.sub(
    r'function saveInlineEdit\(input\) \{[\s\S]*?updateSetOnBackend\(entry\);\n    \}\n\}',
    """function saveInlineEdit(input) {
    input.setAttribute('readonly', 'true');
    input.style.borderBottom = 'none';
    
    const rowIndex = parseInt(input.getAttribute('data-row'));
    const newVal = parseInt(input.value);
    
    if (isNaN(newVal) || newVal <= 0) {
        showToast('Invalid number. Reverting...');
        fetchData(); // Revert UI to old state
        return;
    }
    
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    // Only update if changed
    if (entry.reps !== newVal) {
        entry.reps = newVal;
        updateSetOnBackend(entry);
    }
}""",
    js
)

# Fix renderDailyLog mapping (we missed replacing the HTML string last time too!)
js = re.sub(
    r'    dayData\.forEach\(entry => \{[\s\S]*?dailyLogList\.appendChild\(card\);\n        \}\);\n    \}\);',
    """    dayData.sort((a, b) => {
        if (!a.time && !b.time) return a.rowIndex - b.rowIndex;
        if (!a.time) return -1;
        if (!b.time) return 1;
        return a.time.localeCompare(b.time);
    });

    dayData.forEach((entry) => {
        const card = document.createElement('div');
        card.className = 'log-card';
        card.style.margin = '0';
        card.style.borderBottom = '0.5px solid #E5E5EA';
        
        const iconSvg = EXERCISES[entry.type] || EXERCISES['Push-up'];
        
        card.innerHTML = `
            <div class="log-card-actions" style="position: absolute; top: 0; right: 0; height: 100%; display: flex; z-index: 1;">
                <button class="edit-swipe-btn" onclick="enableEditMode(this, ${entry.rowIndex})" style="background: var(--text-secondary); color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
                <button class="delete-swipe-btn" onclick="confirmDeleteSet(${entry.rowIndex})" style="background: #e74c3c; color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer; border-radius: 0 16px 16px 0;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
            </div>
            <div class="log-card-content" style="position: relative; z-index: 2; background: white; padding: 12px 0; border-radius: 0; display: flex; justify-content: space-between; align-items: center; transition: transform 0.2s ease-out; transform: translateX(0);">
                <div class="log-card-left" style="display: flex; align-items: center; gap: 12px;">
                    <div class="log-icon">${iconSvg}</div>
                    <div class="log-details" style="display: flex; flex-direction: column;">
                        <span class="log-title" style="font-weight: 700; font-size: 1rem;">${entry.type}</span>
                        <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">${entry.time || ''}</span>
                    </div>
                </div>
                <input type="number" class="inline-edit-input" data-row="${entry.rowIndex}" value="${entry.reps}" readonly onblur="saveInlineEdit(this)" onkeydown="if(event.key==='Enter') this.blur();" style="font-size: 1.5rem; font-weight: 800; border: none; background: transparent; width: 70px; text-align: right; color: var(--text-primary); font-family: inherit; outline: none; padding: 0;">
            </div>
        `;
        
        initSwipeActions(card);
        dailyLogList.appendChild(card);
    });""",
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
