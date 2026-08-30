import re

with open('style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Replace the range-toggle-btn block
old_block = """
.range-toggle-btn {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    border: 1.5px solid #ccc;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 700;
    color: #999;
    cursor: pointer;
    transition: all 0.2s;
    background: white;
}
.range-toggle-btn.active {
    border-color: var(--accent-color);
    background: var(--accent-color);
    color: white;
}
"""

new_block = """
.range-toggle-btn {
    width: 22px;
    height: 22px;
    border-radius: 50%;
    border: 1px solid #ddd;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.65rem;
    font-weight: 700;
    color: #999;
    cursor: pointer;
    transition: all 0.2s;
    background: white;
}
.range-toggle-btn.active {
    border-color: var(--accent-color);
    background: var(--accent-color);
    color: white;
}
"""
css = css.replace(old_block.strip(), new_block.strip())

with open('style.css', 'w', encoding='utf-8') as f:
    f.write(css)

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('gap: 12px; padding-top: 16px;', 'gap: 8px; padding-top: 16px;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
