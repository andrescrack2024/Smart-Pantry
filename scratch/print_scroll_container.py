file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("scrollContainer: {")
if idx != -1:
    print("Found scrollContainer at index", idx)
    print(repr(code[idx : idx + 300]))
else:
    print("Could not find scrollContainer.")

idx2 = code.find("profileTabContent: {")
if idx2 != -1:
    print("Found profileTabContent at index", idx2)
    print(repr(code[idx2 : idx2 + 300]))
else:
    print("Could not find profileTabContent.")
