import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

def fix_fetchData_errors(match):
    body = match.group(0)
    
    body = re.sub(r"(\} else if \(json\.authError\) \{\s*showToast\(json\.message\);)", r"\1\n              hideSplashScreen();", body)
    body = re.sub(r"(\} else if \(json\.status === 'error'\) \{\s*showToast\('Error: ' \+ json\.message\);)", r"\1\n              hideSplashScreen();", body)
    
    return body

js = re.sub(r"async function fetchData\(\) \{.*?(?=async function confirmDeleteSet)", fix_fetchData_errors, js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
