import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

pattern = r"if \(weeklyTotal > 0\) \{.*?weeklyLabel\.style\.display = 'none';\n    \}"
new_logic = """// Always show weekly total
    const dayWord = weeklyDaysSet.size === 1 ? 'day' : 'days';
    weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} &nbsp;&nbsp;+${weeklyTotal.toLocaleString()} this week`;
    weeklyLabel.style.display = 'block';"""

js = re.sub(pattern, new_logic, js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
