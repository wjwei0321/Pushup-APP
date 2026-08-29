const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

// 1. Rewrite fetchData parsing
js = js.replace(/trainingData = json\.data\.map.*?;\s*\n\s*\n/s, `trainingData = json.data.map(row => {
                return {
                    dateStr: row[0],
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: row[3] || '',
                    rowIndex: row[4]
                };
            });\n\n`);

// 2. Rewrite calendar groupings
js = js.replace(/const sum = d\.sets\.reduce.*?;/g, `const sum = d.reps;`);
js = js.replace(/todaySetsCount \+= d\.sets\.length;/g, `todaySetsCount += 1;`);

// 3. Rewrite renderDailyLog
js = js.replace(/    dayData\.forEach\(entry => \{.*?entry\.sets\.forEach.*?\}\);\n    \}\);\n/s, `    dayData.sort((a, b) => {
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
        
        card.innerHTML = \`
            <div class="log-card-actions" style="position: absolute; top: 0; right: 0; height: 100%; display: flex; z-index: 1;">
                <button class="edit-swipe-btn" onclick="enableEditMode(this, \${entry.rowIndex})" style="background: var(--text-secondary); color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                </button>
                <button class="delete-swipe-btn" onclick="confirmDeleteSet(\${entry.rowIndex})" style="background: #e74c3c; color: white; border: none; width: 70px; display: flex; align-items: center; justify-content: center; cursor: pointer; border-radius: 0 16px 16px 0;">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path></svg>
                </button>
            </div>
            <div class="log-card-content" style="position: relative; z-index: 2; background: white; padding: 12px 0; border-radius: 0; display: flex; justify-content: space-between; align-items: center; transition: transform 0.2s ease-out; transform: translateX(0);">
                <div class="log-card-left" style="display: flex; align-items: center; gap: 12px;">
                    <div class="log-icon">\${iconSvg}</div>
                    <div class="log-details" style="display: flex; flex-direction: column;">
                        <span class="log-title" style="font-weight: 700; font-size: 1rem;">\${entry.type}</span>
                        <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">\${entry.time || ''}</span>
                    </div>
                </div>
                <input type="number" class="inline-edit-input" data-row="\${entry.rowIndex}" value="\${entry.reps}" readonly onblur="saveInlineEdit(this)" onkeydown="if(event.key==='Enter') this.blur();" style="font-size: 1.5rem; font-weight: 800; border: none; background: transparent; width: 70px; text-align: right; color: var(--text-primary); font-family: inherit; outline: none; padding: 0;">
            </div>
        \`;
        
        initSwipeActions(card);
        dailyLogList.appendChild(card);
    });\n`);

// 4. Update signatures and saveInlineEdit
js = js.replace('function enableEditMode(btn, rowIndex, setIndex)', 'function enableEditMode(btn, rowIndex)');
js = js.replace(/function saveInlineEdit\(input\) \{.*?\n\}\n/s, `function saveInlineEdit(input) {
    input.setAttribute('readonly', 'true');
    input.style.borderBottom = 'none';
    
    const rowIndex = parseInt(input.getAttribute('data-row'));
    const newVal = parseInt(input.value);
    
    if (isNaN(newVal) || newVal <= 0) {
        showToast('Invalid number. Reverting...');
        fetchData();
        return;
    }
    
    const entry = trainingData.find(d => d.rowIndex === rowIndex);
    if (!entry) return;
    
    if (entry.reps !== newVal) {
        entry.reps = newVal;
        updateSetOnBackend(entry);
    }
}\n`);

// 5. Update updateSetOnBackend
js = js.replace(/function updateSetOnBackend\(entry\) \{.*?\n\}\n/s, `function updateSetOnBackend(entry) {
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
}\n`);

// 6. deleteSet and signatures
js = js.replace('function confirmDeleteSet(rowIndex, setIndex)', 'function confirmDeleteSet(rowIndex)');
js = js.replace('deleteTarget = { rowIndex, setIndex };', 'deleteTarget = { rowIndex };');
js = js.replace(/async function deleteSet\(\) \{.*?\n\}\n/s, `async function deleteSet() {
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
}\n`);

// 7. submitWorkout
js = js.replace(/async function submitWorkout\(\) \{.*?\n\}\n/s, `async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = \`\${selectedDate.getFullYear()}/\${String(selectedDate.getMonth()+1).padStart(2, '0')}/\${String(selectedDate.getDate()).padStart(2, '0')}\`;
    const now = new Date();
    const timeStr = \`\${String(now.getHours()).padStart(2, '0')}:\${String(now.getMinutes()).padStart(2, '0')}\`;
    
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
}\n`);

// 8. updateModalStats
js = js.replace(/function updateModalStats\(\) \{.*?\n\}\n/s, `function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = \`\${selectedDate.getFullYear()}/\${String(selectedDate.getMonth()+1).padStart(2, '0')}/\${String(selectedDate.getDate()).padStart(2, '0')}\`;
    const dayRows = trainingData.filter(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = dayRows.length;
    let totalReps = dayRows.reduce((sum, val) => sum + val.reps, 0);
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}\n`);


// 9. API URL Default & Reset Settings Logic
js = js.replace(/let apiUrl = localStorage\.getItem\('pushup_apiUrl'\) \|\| '.*?';/, "let apiUrl = localStorage.getItem('pushup_apiUrl') || 'https://script.google.com/macros/s/AKfycbzygwNK8lzpzJlcFLntcUjhfOiZPQjyHKxssyrjh_pXgVNKd8dSkNrMQSmBCWiP1uG1/exec';");
js = js.replace(/function saveSettings\(\) \{.*?\n    \}\n/s, `function saveSettings() {
    const apiVal = document.getElementById('apiUrl').value.trim();
    const emailVal = document.getElementById('userEmail').value.trim();

    if (apiVal) {
        apiUrl = apiVal;
        localStorage.setItem('pushup_apiUrl', apiUrl);
    } else {
        localStorage.removeItem('pushup_apiUrl');
        apiUrl = 'https://script.google.com/macros/s/AKfycbzygwNK8lzpzJlcFLntcUjhfOiZPQjyHKxssyrjh_pXgVNKd8dSkNrMQSmBCWiP1uG1/exec';
    }\n`);

// 10. renderStats logic
js = js.replace(/    filteredData\.forEach\(d => \{.*?\n    \}\);\n/s, `    filteredData.forEach(d => {
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
    });\n`);

fs.writeFileSync('app.js', js, 'utf8');
