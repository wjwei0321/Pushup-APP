import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

new_css = '''
/* --- Stats View UI --- */
.stats-toggle-btn {
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    color: #bbb;
    background: transparent;
}
.stats-toggle-btn.active {
    background: var(--text-primary);
    color: white;
}

.stats-pills-scroll {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding: 4px 0 16px 0;
    scrollbar-width: none;
    -ms-overflow-style: none;
}
.stats-pills-scroll::-webkit-scrollbar { display: none; }

.stats-exercise-pill {
    padding: 8px 18px;
    border-radius: 50px;
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--text-secondary);
    background: transparent;
    border: 1.5px solid #e0e0e0;
    cursor: pointer;
    white-space: nowrap;
    transition: all 0.2s;
}
.stats-exercise-pill.active {
    background: var(--text-primary);
    color: white;
    border-color: var(--text-primary);
}

.stats-time-filter {
    display: flex;
    background: #111;
    border-radius: 14px;
    padding: 4px;
    gap: 4px;
}
.time-filter-btn {
    flex: 1;
    text-align: center;
    padding: 10px 0;
    border-radius: 10px;
    font-size: 0.85rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.5);
    cursor: pointer;
    transition: all 0.2s;
}
.time-filter-btn.active {
    background: #333;
    color: white;
    box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}
'''

css = re.sub(r'/\* --- Stats View.*', new_css.strip(), css, flags=re.DOTALL)
with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)
