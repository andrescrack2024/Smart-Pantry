import os

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"
with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if "activeTab === 'perfil'" in line or 'activeTab === "perfil"' in line:
        print(f"Line {i+1}: {line.strip()}")
        # print 30 lines after
        for j in range(i+1, min(len(lines), i+60)):
            print(f"  {j+1}: {lines[j].strip()}")
