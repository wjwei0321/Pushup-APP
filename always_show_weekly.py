import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_logic = """      if (weeklyTotal > 0) {
          const dayWord = weeklyDaysSet.size === 1 ? 'day' : 'days';
          weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} &nbsp;&nbsp;+${weeklyTotal.toLocaleString()} this week`;
          weeklyLabel.style.display = 'block';
      } else {
          weeklyLabel.style.display = 'none';
      }"""

new_logic = """      // Always show weekly total
      const dayWord = weeklyDaysSet.size === 1 ? 'day' : 'days';
      weeklyLabel.innerHTML = `${weeklyDaysSet.size} ${dayWord} &nbsp;&nbsp;+${weeklyTotal.toLocaleString()} this week`;
      weeklyLabel.style.display = 'block';"""

js = js.replace(old_logic, new_logic)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
