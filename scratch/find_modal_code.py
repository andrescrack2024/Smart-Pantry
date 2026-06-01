file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

start_marker = "{/* --- MODAL DE COMPARTIR CÓDIGO FAMILIAR"
idx = code.find(start_marker)
if idx != -1:
    print("Found start marker at index", idx)
    # find closing ModalWrapper
    end_marker = "</ModalWrapper>"
    end_idx = code.find(end_marker, idx)
    if end_idx != -1:
        print("Found end marker at index", end_idx)
        print("--- ACTUAL MODAL CODE START ---")
        print(code[idx:end_idx + len(end_marker)])
        print("--- ACTUAL MODAL CODE END ---")
    else:
        print("Could not find end marker after start marker.")
else:
    print("Could not find start marker.")
