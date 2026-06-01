file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("paddingTop: insets.top, backgroundColor: bgMain")
if idx != -1:
    print("Found 'paddingTop: insets.top...' at index", idx)
    start = max(0, idx - 150)
    end = min(len(code), idx + 250)
    print(repr(code[start:end]))
else:
    print("Could not find marker.")
