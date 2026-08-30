import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change the string from `${weeklyDaysSet.size} days, +${weeklyTotal.toLocaleString()} this week` 
# to check pluralization and use ` | `

new_weekly_label = """
        const dayWord = weeklyDaysSet.size === 1 ? 'day' : 'days';
        weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} | +${weeklyTotal.toLocaleString()} this week`;
"""

js = re.sub(r"weeklyLabel\.innerHTML = `\$\{weeklyDaysSet\.size\} days, \+\$\{weeklyTotal\.toLocaleString\(\)\} this week`;", new_weekly_label.strip(), js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
