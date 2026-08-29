import re

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

injection = """    initScrollNav();

    // Sync theme-color with modal state for iOS notch
    const syncThemeColor = () => {
        const meta = document.querySelector('meta[name="theme-color"]');
        if (meta) {
            const isModalOpen = document.querySelector('.modal.show') !== null;
            meta.setAttribute('content', isModalOpen ? '#999999' : '#FFFFFF');
        }
    };
    document.querySelectorAll('.modal').forEach(modal => {
        new MutationObserver(syncThemeColor).observe(modal, { attributes: true, attributeFilter: ['class'] });
    });
    syncThemeColor();"""

js = js.replace("    initScrollNav();", injection)

with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js)
