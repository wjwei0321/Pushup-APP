import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

replacement = """          const maxSets = Math.max(0, ...Object.values(dailyTotals).map(v => v.sets.length));
          const ORANGE_SHADES = [
              '#ffe5b4', '#ffc87c', '#ffb050', '#ff9500', 
              '#e67e22', '#c75b00', '#a64100', '#852d00', 
              '#631d00', '#421000', '#2b0a00', '#140400'
          ];
          for (let i = 0; i < maxSets; i++) {
              const color = ORANGE_SHADES[i % ORANGE_SHADES.length];
              
              const data = sortedDates.map(dateStr => dailyTotals[dateStr].sets[i] || 0);
              datasets.push({
                  label: `Set ${i + 1}`,
                  data: data,
                  backgroundColor: color,"""

js = re.sub(
    r"const maxSets = Math\.max\(0, \.\.\.Object\.values\(dailyTotals\)\.map\(v => v\.sets\.length\)\);\s*for \(let i = 0; i < maxSets; i\+\+\) \{\s*// Generate progressively darker orange for each set\s*const l = Math\.max\(15, 80 - \(i \* 5\)\); \s*const h = Math\.max\(15, 38 - \(i \* 1\.5\)\); \s*const color = `hsl\(\$\{h\}, 100%, \$\{l\}%\)`;\s*const data = sortedDates\.map\(dateStr => dailyTotals\[dateStr\]\.sets\[i\] \|\| 0\);\s*datasets\.push\(\{\s*label: `Set \$\{i \+ 1\}`,\s*data: data,\s*backgroundColor: color,",
    replacement,
    js,
    flags=re.DOTALL
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
