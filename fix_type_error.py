import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix dStr and tStr in map
old_code = """            trainingData = json.data.map(row => {
                let dStr = row[0];
                if (dStr && dStr.includes('T')) {"""

new_code = """            trainingData = json.data.map(row => {
                let dStr = row[0];
                if (dStr && typeof dStr !== 'string') dStr = String(dStr);
                if (dStr && dStr.includes('T')) {"""

js = js.replace(old_code, new_code)


old_code_t = """                let tStr = row[3] || '';
                if (tStr && tStr.includes('T')) {"""

new_code_t = """                let tStr = row[3] || '';
                if (tStr && typeof tStr !== 'string') tStr = String(tStr);
                if (tStr && tStr.includes('T')) {"""

js = js.replace(old_code_t, new_code_t)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
