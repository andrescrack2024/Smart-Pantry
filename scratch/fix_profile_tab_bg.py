import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

target = "style={styles.profileTabContent}"
if target not in code:
    print("Error: Target 'style={styles.profileTabContent}' not found.")
    sys.exit(1)

# Perform replacement
code = code.replace(target, "style={[styles.profileTabContent, { backgroundColor: bgMain }]}")
print("Success: profileTabContent style replaced in-memory.")

native_code = code.replace("\n", os.linesep)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(native_code)

print("PROFILE TAB BACKGROUND CORRECTION SAVED SUCCESSFULLY!")
