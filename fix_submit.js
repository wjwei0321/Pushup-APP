const fs = require('fs');

let js = fs.readFileSync('app.js', 'utf8');

js = js.replace(
    /let dayRow = trainingData\.find.*?try \{/s,
    `// Optimistic UI Update
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
    
    try {`
)

fs.writeFileSync('app.js', js, 'utf8');
