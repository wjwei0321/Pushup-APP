import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix submitWorkout fetch
js = re.sub(
    r'await fetch\(apiUrl, \{\n            method: \'POST\',\n            body: JSON\.stringify\(payload\)\n        \}\);',
    """await fetch(apiUrl, {
            method: 'POST',
            redirect: 'follow',
            headers: {
                'Content-Type': 'text/plain;charset=utf-8',
            },
            body: JSON.stringify(payload)
        });""",
    js
)

# Fix updateSetOnBackend fetch
js = re.sub(
    r'fetch\(apiUrl, \{\n        method: \'POST\',\n        body: JSON\.stringify\(payload\)\n    \}\)',
    """fetch(apiUrl, {
        method: 'POST',
        redirect: 'follow',
        headers: {
            'Content-Type': 'text/plain;charset=utf-8',
        },
        body: JSON.stringify(payload)
    })""",
    js
)

# Fix confirmDeleteSet fetch
js = re.sub(
    r'await fetch\(apiUrl, \{ method: \'POST\', body: JSON\.stringify\(payload\) \}\);',
    """await fetch(apiUrl, { 
                method: 'POST', 
                redirect: 'follow',
                headers: {
                    'Content-Type': 'text/plain;charset=utf-8',
                },
                body: JSON.stringify(payload) 
            });""",
    js
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
