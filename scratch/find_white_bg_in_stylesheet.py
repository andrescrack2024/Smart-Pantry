file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

stylesheet_idx = code.find("const styles = StyleSheet.create")
if stylesheet_idx == -1:
    print("Could not find StyleSheet.create.")
    sys.exit(0)

stylesheet_code = code[stylesheet_idx:]

import re

# Match patterns like: name: { ... backgroundColor: '#...' ... }
# We will match the entire block inside curly braces to find their class name and background
# We can find all keys in the stylesheet and print their background if they are hardcoded light colors
lines = stylesheet_code.split("\n")
current_class = ""
for line in lines:
    if ":" in line and "{" in line and not line.strip().startswith("//"):
        current_class = line.split(":")[0].strip()
    if "backgroundColor:" in line and ("#F7F9FB" in line or "#ffffff" in line or "#fff" in line):
        print(f"Class '{current_class}' has hardcoded background: {line.strip()}")
