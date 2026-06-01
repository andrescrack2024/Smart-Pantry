file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("const handleImageResult = async")
if idx != -1:
    print("Found handleImageResult at index", idx)
    print(repr(code[idx : idx + 1000]))
else:
    print("handleImageResult not found in HomeScreen.js.")
