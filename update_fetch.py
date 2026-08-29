import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start_marker = "trainingData = json.data.filter(row => row[0]).map((row, index) => {"
end_marker = "            renderCalendar(); // Re-render to show indicators"

idx_start = js.find(start_marker)
idx_end = js.find(end_marker)

if idx_start != -1 and idx_end != -1:
    new_code = """trainingData = json.data.map(row => {
                return {
                    dateStr: row[0],
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: row[3] || '',
                    rowIndex: row[4]
                };
            });\n\n"""
    js = js[:idx_start] + new_code + js[idx_end:]

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
