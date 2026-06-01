file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("bottomNav: {")
if idx != -1:
    print("Found bottomNav style at index", idx)
    print(repr(code[idx : idx + 800]))
else:
    print("Could not find bottomNav style in stylesheet.")
