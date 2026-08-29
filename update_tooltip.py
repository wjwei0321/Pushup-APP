import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the tooltip logic
replacement = """            const sets = customData.dailyTotals[dateStrRaw]?.sets || [];
            let setsStr = sets.join(' + ');
            if (sets.length > 1) {
                const total = sets.reduce((a, b) => a + b, 0);
                setsStr += ` = ${total}`;
            }"""

js = re.sub(
    r"const sets = customData\.dailyTotals\[dateStrRaw\]\?\.sets \|\| \[\];\s*const setsStr = sets\.join\(' \+ '\);",
    replacement,
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
