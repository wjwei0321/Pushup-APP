import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """          const maxSets = Math.max(0, ...Object.values(dailyTotals).map(v => v.sets.length));
          for (let i = 0; i < maxSets; i++) {
              // Generate progressively darker orange for each set
              const l = Math.max(15, 80 - (i * 5)); 
              const h = Math.max(15, 38 - (i * 1.5)); 
              const color = `hsl(${h}, 100%, ${l}%)`;
              
              const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets[i] || 0);
              datasets.push({
                  label: `Set ${i + 1}`,
                  data: data,
                  backgroundColor: color,"""

js = re.sub(
    r"const maxSets = Math\.max\(0, \.\.\.Object\.values\(dailyTotals\)\.map\(v => v\.sets\.length\)\);\s*const ORANGE_SHADES = \[.*?\];\s*for \(let i = 0; i < maxSets; i\+\+\) \{\s*const data = sortedDates\.map\(dateStr => dailyTotals\[dateStr\]\.sets\[i\] \|\| 0\);\s*datasets\.push\(\{\s*label: `Set \$\{i \+ 1\}`,\s*data: data,\s*backgroundColor: ORANGE_SHADES\[i % ORANGE_SHADES\.length\],",
    replacement,
    js,
    flags=re.DOTALL
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
