import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

start_marker = "{/* --- MODAL DE COMPARTIR CÓDIGO FAMILIAR"
idx = code.find(start_marker)
if idx == -1:
    print("Error: Start marker not found.")
    sys.exit(1)

end_marker = "</ModalWrapper>"
end_idx = code.find(end_marker, idx)
if end_idx == -1:
    print("Error: End marker not found after start marker.")
    sys.exit(1)

modal_content = code[idx : end_idx + len(end_marker)]

# Count if there are other ModalWrappers inside
modal_wrapper_count = modal_content.count("<ModalWrapper")
closing_wrapper_count = modal_content.count("</ModalWrapper>")

print(f"Modal content length: {len(modal_content)}")
print(f"Contains <ModalWrapper count: {modal_wrapper_count}")
print(f"Contains </ModalWrapper> count: {closing_wrapper_count}")

# Check for specific words to make sure it's the correct modal
has_family_code = "familyCode" in modal_content
has_share_apps = "shareAppsGridAndroid" in modal_content
print(f"Contains 'familyCode': {has_family_code}")
print(f"Contains 'shareAppsGridAndroid': {has_share_apps}")
