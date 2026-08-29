import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace the aggregation logic in renderStats
stats_agg_pattern = re.compile(r'    filteredData\.forEach\(d => \{.*?\n    \}\);\n', re.DOTALL)
new_stats_agg = """    filteredData.forEach(d => {
        if (!dailyTotals[d.dateStr]) dailyTotals[d.dateStr] = { sets: [] };
        dailyTotals[d.dateStr].sets.push(d.reps);
        
        const sum = d.reps;
        grandTotal += sum;
        
        const dDate = new Date(d.dateStr);
        if (dDate >= weekStart && dDate < weekEnd) {
            weeklyTotal += sum;
            weeklyDaysSet.add(d.dateStr);
        }
        
        if (d.dateStr === todayStr) {
            todayTotal += sum;
            todaySetsCount += 1;
        }
    });
"""
js = stats_agg_pattern.sub(new_stats_agg, js)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
