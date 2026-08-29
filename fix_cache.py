import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add cache buster to fetch(apiUrl + "?email="...)
js = js.replace(
    "fetch(apiUrl + '?email=' + encodeURIComponent(userEmail))",
    "fetch(apiUrl + '?email=' + encodeURIComponent(userEmail) + '&cb=' + new Date().getTime())"
)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
