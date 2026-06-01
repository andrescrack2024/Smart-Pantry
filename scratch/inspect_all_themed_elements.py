file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Let's split the code into standard JSX logic and StyleSheet at the bottom
stylesheet_idx = code.find("const styles = StyleSheet.create")
if stylesheet_idx == -1:
    print("Could not find StyleSheet.create.")
    sys.exit(0)

jsx_code = code[:stylesheet_idx]

# Search for hex colors in inline style patterns like background: '#...', color: '#...'
# Or style={{ ... }} with hardcoded colors
import re

# Match strings like "#F7F9FB", "#ffffff", "#1E1E1E", "#121212", etc.
hex_pattern = re.compile(r"['\"]#([A-Fa-f0-9]{3,8})['\"]")
matches = hex_pattern.findall(jsx_code)

print("Hex colors found in JSX code:")
unique_matches = set(matches)
for m in sorted(unique_matches):
    color = f"#{m}"
    # Count occurrences
    count = jsx_code.count(color)
    print(f"  {color}: {count} occurrences")

print("\nDetail of some inline styles that might need attention:")
# Search for styled containers with inline colors
inline_style_pattern = re.compile(r"style=\{\[[^\]]*backgroundColor:\s*['\"]#[^'\"]*['\"][^\]]*\]\}")
for m in inline_style_pattern.finditer(jsx_code):
    print("Found inline styles with hardcoded bg:", m.group(0))
