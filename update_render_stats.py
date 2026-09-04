import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_code = """    // Bottom Exercise Tabs
    const filterContainer = document.getElementById('statsExerciseFilter');
    filterContainer.innerHTML = '';
    Object.keys(EXERCISES).forEach(ex => {
        
        const iconWrap = document.createElement('div');
        iconWrap.style.cssText = 'width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; padding: 6px; cursor: pointer; transition: all 0.2s; flex-shrink: 0;';
        
        if (currentStatsExercise === ex) {
            iconWrap.style.background = '#f39c12';
            iconWrap.style.color = '#fff';
            iconWrap.style.boxShadow = '0 4px 10px rgba(243, 156, 18, 0.4)';
        } else {
            iconWrap.style.background = 'transparent';
            iconWrap.style.color = '#999';
            iconWrap.style.boxShadow = 'none';
        }
        iconWrap.innerHTML = EXERCISES[ex].replace('width="24"', 'width="18"').replace('height="24"', 'height="18"');
        iconWrap.onclick = () => setStatsExercise(ex);
        filterContainer.appendChild(iconWrap);
    });"""


new_code = """    // Bottom Exercise Tabs
    const filterContainer = document.getElementById('statsExerciseFilter');
    if (filterContainer.children.length === 0) {
        Object.keys(EXERCISES).forEach(ex => {
            const iconWrap = document.createElement('div');
            iconWrap.dataset.exercise = ex;
            iconWrap.style.cssText = 'width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center; justify-content: center; padding: 6px; cursor: pointer; transition: all 0.2s; flex-shrink: 0;';
            iconWrap.innerHTML = EXERCISES[ex].replace('width="24"', 'width="18"').replace('height="24"', 'height="18"');
            iconWrap.onclick = () => setStatsExercise(ex);
            filterContainer.appendChild(iconWrap);
        });
    }
    
    Array.from(filterContainer.children).forEach(iconWrap => {
        if (currentStatsExercise === iconWrap.dataset.exercise) {
            iconWrap.style.background = '#f39c12';
            iconWrap.style.color = '#fff';
            iconWrap.style.boxShadow = '0 4px 10px rgba(243, 156, 18, 0.4)';
        } else {
            iconWrap.style.background = 'transparent';
            iconWrap.style.color = '#999';
            iconWrap.style.boxShadow = 'none';
        }
    });"""

js = js.replace(old_code, new_code)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
