const fs = require('fs');
let html = fs.readFileSync('index.html', 'utf8');

const modalStart = '<div class="modal" id="settingsModal">';
const modalEnd = '<div class="toast" id="toast">';
const idx1 = html.indexOf(modalStart);
const idx2 = html.indexOf(modalEnd);

if (idx1 !== -1 && idx2 !== -1) {
    const newModal = `<div class="modal" id="settingsModal">
        <div class="modal-content" style="padding: 0; background: #fafafa; border-radius: 20px 20px 0 0; display: flex; flex-direction: column;">
            <div style="padding: calc(20px + env(safe-area-inset-top, 20px)) 20px 20px 20px; display: flex; flex-direction: column; touch-action: none; position: relative;">
                <div style="width: 36px; height: 5px; background: #ddd; border-radius: 3px; align-self: center; margin-bottom: 15px;"></div>
                <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                    <h3 style="margin: 0; font-size: 1.4rem; font-weight: 700;">Settings & Profile</h3>
                    <div id="currentUserDisplay" style="margin-top: 5px; font-size: 0.9rem; color: var(--accent-color); font-weight: 600;">Not logged in</div>
                </div>
            </div>
            <div style="padding: 10px 20px 40px 20px;">
                <label style="display: block; font-weight: 600; margin-bottom: 8px; font-size: 0.9rem;">Your Email (for sync)</label>
                <input type="email" id="userEmail" placeholder="e.g. user@gmail.com" style="width: 100%; padding: 15px; border-radius: 12px; border: 1.5px solid var(--border-color); background: var(--card-bg); font-family: Outfit; font-size: 1rem; margin-bottom: 25px; box-sizing: border-box;">
                
                <button onclick="saveSettings()" style="width: 100%; padding: 16px; border-radius: 14px; border: none; background: #111; color: white; font-family: Outfit; font-weight: 700; font-size: 1.1rem; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">Save & Sync</button>
            </div>
        </div>
    </div>
    `;
    html = html.substring(0, idx1) + newModal + html.substring(idx2);
    html = html.replace(/v=4\.29/g, 'v=4.30');
    fs.writeFileSync('index.html', html, 'utf8');
}
