import os

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for idx in range(2830, 2950):
    if idx < len(lines):
        line = lines[idx].strip()
        safe_line = line.encode('ascii', errors='replace').decode('ascii')
        print(f"{idx+1}: {safe_line}")
