file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

idx = code.find('customAlert("Error", "No se pudo actualizar la foto de perfil.")')
if idx != -1:
    print("Found error message at index", idx)
    # Search backwards for the function start
    # Let's search for "const " or "function " or "async "
    # We'll print 5000 characters before the error message, but filtered to show actual code lines (omitting empty lines)
    snippet = code[idx - 5000 : idx]
    lines = snippet.split("\n")
    non_empty_lines = [line.strip() for line in lines if line.strip() != ""]
    # Show the last 100 non-empty lines before the error
    print("--- PREVIOUS CODE LINES ---")
    for line in non_empty_lines[-70:]:
        print(line)
else:
    print("Error message not found in HomeScreen.js.")
