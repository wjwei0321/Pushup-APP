with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

js = js.replace("if (!exList.includes(ex)) return;", "")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
