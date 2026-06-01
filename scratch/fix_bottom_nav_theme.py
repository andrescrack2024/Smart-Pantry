import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

# Find the start index of styles.bottomNav in JSX
start_marker = "styles.bottomNav"
start_idx = code.find(start_marker)
if start_idx == -1:
    print("Error: styles.bottomNav not found in JSX.")
    sys.exit(1)

# Find the opening brace '{' after start_idx
open_brace_idx = code.find("{", start_idx)
if open_brace_idx == -1:
    print("Error: Opening brace not found after styles.bottomNav.")
    sys.exit(1)

# Find the closing brace '}' of the style object
close_brace_idx = code.find("}", open_brace_idx)
if close_brace_idx == -1:
    print("Error: Closing brace not found.")
    sys.exit(1)

# Let's slice the exact inline style object
old_inline_style = code[open_brace_idx : close_brace_idx + 1]
print("Found old inline styles:")
print(repr(old_inline_style))

# Replace with the new theme-aware properties
new_inline_style = """{ 

          height: bottomNavHeight, 

          paddingBottom: Math.max(insets.bottom, 10),

          backgroundColor: bgCard,

          borderTopColor: borderCard

        }"""

# Reconstruct the code
part1 = code[:open_brace_idx]
part2 = code[close_brace_idx + 1 :]
code = part1 + new_inline_style + part2

native_code = code.replace("\n", os.linesep)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(native_code)

print("BOTTOM NAV THEME FIX SAVED SUCCESSFULLY!")
