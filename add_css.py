import os

with open('style.css', 'a', encoding='utf-8') as f:
    f.write("""
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
""")
