import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

replacements = [
    (
        "style={styles.historyCard}",
        "style={[styles.historyCard, { backgroundColor: bgCard, borderColor: borderCard }]}",
    ),
    (
        "style={styles.historyAction}",
        "style={[styles.historyAction, { color: textPrimary }]}",
    ),
    (
        "style={styles.historyTime}",
        "style={[styles.historyTime, { color: textSecondary }]}",
    ),
]

all_ok = True
for old, new in replacements:
    if old not in code:
        print(f"Error: Target '{old}' not found.")
        all_ok = False
    else:
        code = code.replace(old, new)
        print(f"Success: Replaced '{old}' with '{new}'.")

if all_ok:
    native_code = code.replace("\n", os.linesep)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(native_code)
    print("HISTORY THEME INTEGRATED SUCCESSFULLY!")
else:
    print("ABORTED: History theme fixes could not be applied.")
