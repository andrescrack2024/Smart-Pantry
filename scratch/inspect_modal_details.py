import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

import re

# Find ModalWrappers and print their container view style definitions
modal_matches = re.finditer(
    r"<ModalWrapper\s+visible={([^}]+)}.*?<ModalWrapper", code, re.DOTALL
)

# Since we want to find all of them, let's just find each ModalWrapper block
# Let's search for '<ModalWrapper' and get the next 1500 chars to check their container styles
idx = 0
while True:
    idx = code.find("<ModalWrapper", idx)
    if idx == -1:
        break
    print(f"\nModal starting at index {idx}:")
    snippet = code[idx : idx + 1000]
    # Find container view (e.g. style={[styles.modalContent, ...]} or similar)
    lines = snippet.split("\n")
    for line in lines[:25]:
        if "style=" in line or "placeholder=" in line or "color=" in line:
            print(f"  {line.strip()}")
    idx += len("<ModalWrapper")
