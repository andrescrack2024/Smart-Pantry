import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Normalize line endings
code = code.replace("\r\n", "\n")

replacements = []

# 1. Detail Category Bubble (with double newlines)
old_bubble = """                      style={[

                        styles.detailCategoryBubble, 

                        editCategory === cat && { backgroundColor: themeColor, borderColor: themeColor }

                      ]}"""

new_bubble = """                      style={[

                        styles.detailCategoryBubble, 

                        { backgroundColor: isDark ? '#242424' : '#F8FAFC', borderColor: isDark ? '#3D3D3D' : '#E2E8F0' },

                        editCategory === cat && { backgroundColor: themeColor, borderColor: themeColor }

                      ]}"""

replacements.append(("Detail category bubble", old_bubble, new_bubble))

# 2. Detail Category Bubble Text (with double newlines)
old_bubble_text = """                      <Text style={[

                        styles.detailCategoryBubbleText, 

                        editCategory === cat && { color: '#fff', fontWeight: '800' }

                      ]}>{cat}</Text>"""

new_bubble_text = """                      <Text style={[

                        styles.detailCategoryBubbleText, 

                        { color: isDark ? '#CAC4D0' : '#64748B' },

                        editCategory === cat && { color: '#fff', fontWeight: '800' }

                      ]}>{cat}</Text>"""

replacements.append(("Detail category bubble text", old_bubble_text, new_bubble_text))

# 3. Detail Image Container Placeholder
old_image_placeholder = """                  <View style={[styles.detailImageContainer, { justifyContent: 'center', alignItems: 'center', backgroundColor: '#F8FAFC' }]}>"""

new_image_placeholder = """                  <View style={[styles.detailImageContainer, { justifyContent: 'center', alignItems: 'center', backgroundColor: isDark ? '#242424' : '#F8FAFC', borderColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}>"""

replacements.append(("Detail image placeholder", old_image_placeholder, new_image_placeholder))

# 4. Quantity Editor Container
old_qty_container = """                  <View style={[styles.quantityEditorContainer, { flex: 1, marginBottom: 14 }]}>"""

new_qty_container = """                  <View style={[styles.quantityEditorContainer, { flex: 1, marginBottom: 14, backgroundColor: isDark ? '#242424' : '#F8FAFC', borderColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}>"""

replacements.append(("Quantity editor container", old_qty_container, new_qty_container))

all_ok = True
for name, old, new in replacements:
    old_norm = old.replace("\r\n", "\n")
    if old_norm not in code:
        print(f"Error: Target '{name}' not found exactly.")
        all_ok = False
    else:
        # Since quantity editor container appears twice, we replace both (which is what we want!)
        code = code.replace(old_norm, new.replace("\r\n", "\n"))
        print(f"Success: Target '{name}' replaced.")

if all_ok:
    native_code = code.replace("\n", os.linesep)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(native_code)
    print("ALL DETAIL MODAL THEME FIXES APPLIED SUCCESSFULLY!")
else:
    print("ABORTED: Detail modal theme fixes could not be applied.")
