import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Update updateModalStats
stats_pattern = re.compile(r'function updateModalStats\(\) \{.*?\n\}\n', re.DOTALL)
new_stats = """function updateModalStats() {
    if (!selectedExerciseForLog) return;
    const dateStr = ${selectedDate.getFullYear()}//;
    const dayRows = trainingData.filter(d => d.dateStr === dateStr && d.type === selectedExerciseForLog);
    
    let sets = dayRows.length;
    let totalReps = dayRows.reduce((sum, val) => sum + val.reps, 0);
    
    document.getElementById('modalSetsToday').textContent = sets;
    document.getElementById('modalTotalRepsToday').textContent = totalReps;
}
"""
js = stats_pattern.sub(new_stats, js)


# 2. Update submitWorkout
submit_pattern = re.compile(r'async function submitWorkout\(\) \{.*?\n\}\n', re.DOTALL)
new_submit = """async function submitWorkout() {
    if (!selectedExerciseForLog) return alert('Please select an exercise.');
    const reps = document.getElementById('workoutRepsDisplay').textContent;
    if (!reps || isNaN(reps) || parseInt(reps) <= 0) return alert('Please enter valid reps.');
    
    const dateStr = ${selectedDate.getFullYear()}//;
    
    const now = new Date();
    const timeStr = ${String(now.getHours()).padStart(2, '0')}:;
    
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
}
"""
js = submit_pattern.sub(new_submit, js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
