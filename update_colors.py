import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Change interval growth colors
js = js.replace("color = '#e74c3c'; // Growth = Red", "color = '#f23645'; // Growth = Red")
js = js.replace("color = '#2ecc71'; // Decrease = Green", "color = '#2bb596'; // Decrease = Green")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
