import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I need to find the fetchData function and carefully restore the hideSplashScreen calls.
# It is much safer to just patch the specific lines in fetchData.

def fix_fetchData(match):
    body = match.group(0)
    
    # After renderDailyLog()
    if "renderDailyLog(); // Re-render list" in body:
        body = body.replace("renderDailyLog(); // Re-render list", "renderDailyLog(); // Re-render list\n            hideSplashScreen();")
        
    # After json.authError block
    if "} else if (json.authError) {" in body:
        body = body.replace("} else if (json.authError) {\n              showToast(json.message);", "} else if (json.authError) {\n              showToast(json.message);\n              hideSplashScreen();")
        
    # After json.status === 'error'
    if "} else if (json.status === 'error') {" in body:
        body = body.replace("} else if (json.status === 'error') {\n              showToast('Error: ' + json.message);", "} else if (json.status === 'error') {\n              showToast('Error: ' + json.message);\n              hideSplashScreen();")
        
    return body

js = re.sub(r"async function fetchData\(\) \{.*?(?=async function confirmDeleteSet)", fix_fetchData, js, flags=re.DOTALL)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
