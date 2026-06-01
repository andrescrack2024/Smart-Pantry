file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("style={styles.profileTabContent}")
if idx != -1:
    print("Found profileTabContent in JSX at index", idx)
    print(repr(code[idx - 100 : idx + 300]))
else:
    print("profileTabContent not found in JSX.")
