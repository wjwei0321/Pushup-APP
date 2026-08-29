import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

bad_saveSettings = """function saveSettings() {
    const apiVal = document.getElementById('apiUrl').value.trim();
    const emailVal = document.getElementById('userEmail').value.trim();

    if (apiVal) {
        apiUrl = apiVal;
        localStorage.setItem('pushup_apiUrl', apiUrl);
    }

    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }

    settingsModal.classList.remove('show');
    setTimeout(() => settingsModal.style.display = 'none', 300);
    
    // Refresh data
    showSplashScreen();
    fetchData();
}"""

good_saveSettings = """function saveSettings() {
    const emailVal = document.getElementById('userEmail').value.trim();

    if (emailVal) {
        userEmail = emailVal;
        localStorage.setItem('pushup_userEmail', userEmail);
    }

    settingsModal.classList.remove('show');
    setTimeout(() => settingsModal.style.display = 'none', 300);
    
    // Refresh data
    showSplashScreen();
    fetchData();
}"""

if bad_saveSettings in js:
    js = js.replace(bad_saveSettings, good_saveSettings)
    with open('app.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("Replaced!")
else:
    print("Not found! Let's search.")
    idx = js.find("function saveSettings()")
    print(js[idx:idx+400])
