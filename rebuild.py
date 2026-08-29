import re

with open('app.js', 'r', encoding='utf-8', errors='replace') as f:
    js = f.read()

# 1. Update API URL and remove from openSettings & saveSettings
js = js.replace(
    "let apiUrl = localStorage.getItem('pushup_apiUrl') || 'https://script.google.com/macros/s/AKfycbxJjXFEU8cZ_ZMxKlRcm03uGKWzLvjahLQlZpLznUq2diICcQvF4qZM3ryiumwyqxjJ/exec';",
    "let apiUrl = 'https://script.google.com/macros/s/AKfycbzygwNK8lzpzJlcFLntcUjhfOiZPQjyHKxssyrjh_pXgVNKd8dSkNrMQSmBCWiP1uG1/exec';"
)

js = js.replace(
    "document.getElementById('apiUrl').value = apiUrl;\n    document.getElementById('userEmail').value = userEmail;",
    "document.getElementById('userEmail').value = userEmail;"
)

js = js.replace(
"""function saveSettings() {
    const apiVal = document.getElementById('apiUrl').value.trim();
    const emailVal = document.getElementById('userEmail').value.trim();

    if (apiVal) {
        apiUrl = apiVal;
        localStorage.setItem('pushup_apiUrl', apiUrl);
    }
    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }
    
    settingsModal.classList.remove('show');
    setTimeout(() => { settingsModal.style.display = 'none'; }, 300);
    
    // Refresh data
    showSplashScreen();
    fetchData();
}""",
"""function saveSettings() {
    const emailVal = document.getElementById('userEmail').value.trim();

    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }
    
    settingsModal.classList.remove('show');
    setTimeout(() => { settingsModal.style.display = 'none'; }, 300);
    
    // Refresh data
    showSplashScreen();
    fetchData();
}""")

# 2. Update fetchData mapping
js = js.replace(
"""            trainingData = json.data.filter(row => row[0]).map((row, index) => {
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
                    rowIndex: row[8], // Sheet row
                    dateStr: dateStr,
                    type: row[1],
                    sets: sets
                };
            });""",
"""            trainingData = json.data.map(row => {
                return {
                    dateStr: row[0],
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: row[3] || '',
                    rowIndex: row[4]
                };
            });""")


# 3. Calendar logic updates
js = js.replace(
    "const sum = d.sets.reduce((a, b) => a + b, 0);",
    "const sum = d.reps || 0;"
)
js = js.replace(
    "todaySetsCount += d.sets.length;",
    "todaySetsCount += 1;"
)


# 4. updateModalStats
js = js.replace(
"""function updateModalStats() {
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
}""",
"""function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    const dayRows = trainingData.filter(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = dayRows.length;
    let totalReps = dayRows.reduce((sum, val) => sum + val.reps, 0);
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}""")

# 5. submitWorkout
js = js.replace(
"""async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = `${selectedDate.getFullYear()}/${String(selectedDate.getMonth()+1).padStart(2, '0')}/${String(selectedDate.getDate()).padStart(2, '0')}`;
    
    const payload = {
        action: 'log',
        email: userEmail,
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
        // Silent success
    } catch (e) {
        console.error(e);
        hideSplashScreen();
    }
}""",
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
        rowIndex: 999999 + Math.random(), // Temporary
        dateStr: dateStr,
        type: selectedExerciseForLog,
        reps: parseInt(reps),
        time: timeStr
    });
    
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
        fetchData(); // Sync exact state and row index
    } catch (e) {
        console.error(e);
        hideSplashScreen();
    }
}""")

# 6. Delete and Edit APIs
js = js.replace("function enableEditMode(btn, rowIndex, setIndex)", "function enableEditMode(btn, rowIndex)")
js = js.replace(
"""function saveInlineEdit(input) {
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
}""",
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
}""")

js = js.replace(
"""function updateSetOnBackend(entry) {
    showSplashScreen();
    
    const payload = {
        action: 'editRow',
        email: userEmail,
        date: entry.dateStr,
        type: entry.type,
        sets: entry.sets,
        rowIndex: entry.rowIndex
    };
    
    fetch(apiUrl, {
        method: 'POST',
        body: JSON.stringify(payload)
    }).then(r => r.json()).then(res => {
        if(res.status === 'success') {
            showToast('Saved');
            hideSplashScreen();
            renderCalendar();
        } else {
            showToast('Error');
            hideSplashScreen();
        }
    }).catch(e => {
        hideSplashScreen();
        showToast('Error');
    });
}""",
"""function updateSetOnBackend(entry) {
    showSplashScreen();
    const payload = {
        action: 'edit',
        rowIndex: entry.rowIndex,
        count: entry.reps
    };
    
    fetch(apiUrl, {
        method: 'POST',
        body: JSON.stringify(payload)
    }).then(r => r.json()).then(res => {
        if(res.status === 'success') {
            showToast('Saved');
            fetchData();
        } else {
            showToast('Error');
            fetchData();
        }
    }).catch(e => {
        hideSplashScreen();
        showToast('Error');
    });
}""")


js = js.replace("function confirmDeleteSet(rowIndex, setIndex)", "function confirmDeleteSet(rowIndex)")
js = js.replace("deleteTarget = { rowIndex, setIndex };", "deleteTarget = { rowIndex };")
js = js.replace(
"""async function deleteSet() {
    if (!deleteTarget) return;
    closeDeleteModal();
    showSplashScreen();
    
    const entry = trainingData.find(d => d.rowIndex === deleteTarget.rowIndex);
    if (entry) {
        entry.sets.splice(deleteTarget.setIndex, 1);
        
        // Optimistic
        renderDailyLog();
        renderCalendar();
        
        const payload = {
            action: 'editRow',
            email: userEmail,
            date: entry.dateStr,
            type: entry.type,
            sets: entry.sets,
            rowIndex: entry.rowIndex
        };
        
        try {
            await fetch(apiUrl, {
                method: 'POST',
                body: JSON.stringify(payload)
            });
            showToast('Deleted');
            hideSplashScreen();
            if (entry.sets.length === 0) fetchData(); // Hard refresh if row emptied
        } catch (e) {
            hideSplashScreen();
            showToast('Error deleting record');
            fetchData();
        }
    }
    
    deleteTarget = null;
}""",
"""async function deleteSet() {
    if (!deleteTarget) return;
    closeDeleteModal();
    showSplashScreen();
    
    const payload = {
        action: 'delete',
        rowIndex: deleteTarget.rowIndex
    };
    
    try {
        const res = await fetch(apiUrl, {
            method: 'POST',
            body: JSON.stringify(payload)
        });
        const result = await res.json();
        
        if (result.status === 'success') {
            showToast('Deleted');
            fetchData();
        } else {
            showToast('Error: ' + result.message);
        }
    } catch (e) {
        console.error(e);
        hideSplashScreen();
        showToast('Error deleting record');
    }
    
    deleteTarget = null;
}""")

# 7. renderDailyLog
js = js.replace(
"""    dayData.forEach(entry => {
        entry.sets.forEach((repCount, setIndex) => {
            const card = document.createElement('div');
            card.className = 'log-card';
            card.style.margin = '0';
            card.style.borderBottom = '0.5px solid #E5E5EA';
            
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
                <div class="log-card-content" style="position: relative; z-index: 2; background: white; padding: 12px 0; border-radius: 0; display: flex; justify-content: space-between; align-items: center; transition: transform 0.2s ease-out; transform: translateX(0);">
                    <div class="log-card-left" style="display: flex; align-items: center; gap: 12px;">
                        <div class="log-icon">${iconSvg}</div>
                        <div class="log-details" style="display: flex; flex-direction: column;">
                            <span class="log-title" style="font-weight: 700; font-size: 1rem;">${entry.type}</span>
                            <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">Set ${setIndex + 1}</span>
                        </div>
                    </div>
                    <input type="number" class="inline-edit-input" data-row="${entry.rowIndex}" data-set="${setIndex}" value="${repCount}" readonly onblur="saveInlineEdit(this)" onkeydown="if(event.key==='Enter') this.blur();" style="font-size: 1.5rem; font-weight: 800; border: none; background: transparent; width: 70px; text-align: right; color: var(--text-primary); font-family: inherit; outline: none; padding: 0;">
                </div>
            `;
            
            initSwipeActions(card);
            
            dailyLogList.appendChild(card);
        });
    });""",
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
    });""")


# 8. renderStats
js = js.replace(
"""    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = { sets: [] };
        dailyTotals[d.dateStr].sets.push(...d.sets);
        
        const sum = d.sets.reduce((a, b) => a + b, 0);
        grandTotal += sum;
        
        const dDate = new Date(d.dateStr);
        if (dDate >= weekStart && dDate < weekEnd) {
            weeklyTotal += sum;
            weeklyDaysSet.add(d.dateStr);
        }
        
        if (d.dateStr === todayStr) {
            todayTotal += sum;
            todaySetsCount += d.sets.length;
        }
    });""",
"""    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = { sets: [] };
        dailyTotals[d.dateStr].sets.push(d.reps);
        
        const sum = d.reps;
        grandTotal += sum;
        
        const dDate = new Date(d.dateStr);
        if (dDate >= weekStart && dDate < weekEnd) {
            weeklyTotal += sum;
            weeklyDaysSet.add(d.dateStr);
        }
        
        if (d.dateStr === todayStr) {
            todayTotal += sum;
            todaySetsCount += 1;
        }
    });""")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
