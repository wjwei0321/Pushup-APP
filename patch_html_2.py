import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace SETS and TOTAL
html = html.replace('SETS</div>', 'SETS</div>').replace('SETS', '<span data-i18n="sets_upper">SETS</span>')
html = html.replace('TOTAL</div>', 'TOTAL</div>').replace('TOTAL', '<span data-i18n="total_upper">TOTAL</span>')

# Not logged in
html = html.replace('Not logged in', '<span data-i18n="not_logged_in">Not logged in</span>')

# Select Exercises
html = html.replace('>Select Exercises<', ' data-i18n="select_exercises">Select Exercises<')

# C (Clear button) -> Let's keep it C, but add i18n
html = html.replace('>C<', ' data-i18n="clear_btn">C<')

# API URL Label
html = html.replace('>API URL<', ' data-i18n="api_url">API URL<')

# Logged successfully inside JS `showToast("Logged successfully!")` will be handled in JS.

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
