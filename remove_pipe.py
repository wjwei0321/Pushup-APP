import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change ` | ` to `  ` (two spaces or one space)
old_str = "weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} | +${weeklyTotal.toLocaleString()} this week`;"
new_str = "weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} &nbsp;&nbsp;+${weeklyTotal.toLocaleString()} this week`;"

js = js.replace(old_str, new_str)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
