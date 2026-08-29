import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add tallying logic
tally_logic = """    dayData.sort((a, b) => {
        if (!a.time && !b.time) return a.rowIndex - b.rowIndex;
        if (!a.time) return -1;
        if (!b.time) return 1;
        return a.time.localeCompare(b.time);
    });

    const typeSetCounts = {};
    dayData.forEach((entry) => {
        if (!typeSetCounts[entry.type]) {
            typeSetCounts[entry.type] = 1;
        } else {
            typeSetCounts[entry.type]++;
        }
        entry.setNumber = typeSetCounts[entry.type];
    });"""

js = re.sub(
    r"dayData\.sort\(\(a, b\) => \{.*?\}\);",
    tally_logic,
    js,
    flags=re.DOTALL
)

# Modify time rendering
render_logic = """<span class="log-title" style="font-weight: 700; font-size: 1rem;">${entry.type}</span>
                          <span class="log-time" style="font-size: 0.8rem; color: var(--text-secondary);">${entry.time ? `Set ${entry.setNumber}｜${entry.time}` : `Set ${entry.setNumber}`}</span>"""

js = re.sub(
    r"<span class=\"log-title\"[^>]*>\$\{entry\.type\}</span>\s*<span class=\"log-time\"[^>]*>\$\{entry\.time\s*\|\|\s*''\}</span>",
    render_logic,
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
