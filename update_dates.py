import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

target = """            trainingData = json.data.map(row => {
                return {
                    dateStr: row[0],
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: row[3] || '',
                    rowIndex: row[4]
                };
            });"""

replacement = """            trainingData = json.data.map(row => {
                let dStr = row[0];
                if (dStr && dStr.includes('T')) {
                    const d = new Date(dStr);
                    dStr = `${d.getFullYear()}/${String(d.getMonth()+1).padStart(2, '0')}/${String(d.getDate()).padStart(2, '0')}`;
                } else if (dStr && dStr.includes('-')) {
                    dStr = dStr.replace(/-/g, '/');
                }
                
                let tStr = row[3] || '';
                if (tStr && tStr.includes('T')) {
                    const d = new Date(tStr);
                    tStr = `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
                }
                
                return {
                    dateStr: dStr,
                    type: row[1],
                    reps: parseInt(row[2]) || 0,
                    time: tStr,
                    rowIndex: row[4]
                };
            });"""

if target in js:
    js = js.replace(target, replacement)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced!")
else:
    print("Not found! Here is what we have near there:")
    idx = js.find("trainingData = json.data.map")
    print(js[idx:idx+200])
