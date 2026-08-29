import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add showSplashScreen function next to hideSplashScreen
js = js.replace(
    "function hideSplashScreen() {",
    "function showSplashScreen() {\n    const splash = document.getElementById('splashScreen');\n    if (splash) {\n        splash.style.display = 'flex';\n    }\n}\n\nfunction hideSplashScreen() {"
)

# Remove the ugly alert in confirmDeleteSet
js = js.replace(
    "alert('Cannot find record to delete. RowIndex: ' + rawRowIndex);",
    "console.error('Cannot find record to delete. RowIndex: ' + rawRowIndex);"
)
js = js.replace(
    "alert('Delete error: ' + e.toString());",
    "console.error('Delete error: ' + e.toString());\n        showToast('Error deleting record');"
)


with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
