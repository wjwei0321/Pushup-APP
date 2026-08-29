import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

start = js.find("function saveSettings()")
end = js.find("}", start) + 1

if start != -1:
    good_saveSettings = """function saveSettings() {
    const emailVal = document.getElementById('userEmail').value.trim();

    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }

    settingsModal.classList.remove('show');
    setTimeout(() => { settingsModal.style.display = 'none'; }, 300);
    
    // Refresh data
    showSplashScreen();
    fetchData();
}"""
    
    js = js[:start] + good_saveSettings + js[js.find("}", js.find("showSplashScreen();", start)) + 1:]
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced safely!")
