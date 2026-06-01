file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

for style_name in ["historyCard", "historyAction", "historyTime"]:
    idx = code.find(f"{style_name}: {{")
    if idx != -1:
        print(f"Found {style_name} in stylesheet at index", idx)
        print(repr(code[idx : idx + 300]))
        print("-" * 50)
    else:
        print(f"Could not find {style_name} in stylesheet.")
