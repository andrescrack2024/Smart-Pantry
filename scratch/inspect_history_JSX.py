file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("style={styles.historyCard}")
if idx != -1:
    print("Found styles.historyCard in JSX at index", idx)
    print(repr(code[idx - 150 : idx + 400]))
else:
    print("styles.historyCard not found in JSX.")
