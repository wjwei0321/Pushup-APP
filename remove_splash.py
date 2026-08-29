import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Remove showSplashScreen and hideSplashScreen from confirmDeleteSet
js = js.replace("            showSplashScreen();\n", "")
js = js.replace("            hideSplashScreen();\n", "")

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
