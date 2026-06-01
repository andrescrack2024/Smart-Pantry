file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find("styles.detailCategoryBubble,")
if idx != -1:
    print("Found 'styles.detailCategoryBubble,' at index", idx)
    # Print the characters before and after to see exact spaces/newlines
    start = max(0, idx - 100)
    end = min(len(code), idx + 200)
    print(repr(code[start:end]))
else:
    print("Could not find 'styles.detailCategoryBubble,'")
