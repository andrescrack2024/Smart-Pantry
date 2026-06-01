file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = 0
while True:
    idx = code.find("launchImageLibraryAsync", idx)
    if idx == -1:
        break
    print(f"\nlaunchImageLibraryAsync found at index {idx}:")
    print(repr(code[idx - 100 : idx + 300]))
    idx += len("launchImageLibraryAsync")
