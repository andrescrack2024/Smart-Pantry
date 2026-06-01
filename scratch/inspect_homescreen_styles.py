file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Let's search for all Modal content containers and check if they use dynamic style overlays
# Example: <ModalWrapper or <Modal

import re

modals = re.findall(r"<ModalWrapper[^>]*>.*?</ModalWrapper>", code, re.DOTALL)
print(f"Found {len(modals)} ModalWrappers in HomeScreen.js:")
for i, m in enumerate(modals):
    # Print the outer container view inside the modal
    outer_view = re.search(r"<View[^>]*>", m)
    first_few_lines = "\n".join(m.split("\n")[:10])
    print(f"ModalWrapper {i+1}:")
    print(first_few_lines)
    print("-" * 40)
