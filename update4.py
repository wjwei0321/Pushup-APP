import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the broken renderDailyLog
start_marker = "    dayData.sort((a, b) => {"
end_marker = "function initSwipeActions(card) {"

idx_start = js.find(start_marker)
idx_end = js.find(end_marker)

if idx_start != -1 and idx_end != -1:
    new_render = """    dayData.sort((a, b) => {
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
    });
}

"""
    js = js[:idx_start] + new_render + js[idx_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
