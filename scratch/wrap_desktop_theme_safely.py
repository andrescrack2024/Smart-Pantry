import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Normalize to LF
code = code.replace("\r\n", "\n")

# 1. Find the return statement start dynamically
target_insets = "paddingTop: insets.top, backgroundColor: bgMain"
idx_insets = code.find(target_insets)
if idx_insets == -1:
    print("Error: target_insets not found.")
    sys.exit(1)

idx_return = code.rfind("return (", 0, idx_insets)
if idx_return == -1:
    print("Error: return ( not found.")
    sys.exit(1)

idx_desktop = code.find("isDesktopWeb ? {", idx_insets)
if idx_desktop == -1:
    print("Error: isDesktopWeb ? { not found.")
    sys.exit(1)

print(f"Indices: return={idx_return}, insets={idx_insets}, desktop={idx_desktop}")

# Verify what we are replacing
original_start_block = code[idx_return:idx_desktop]
print("--- MATCHED START BLOCK REPR ---")
print(repr(original_start_block))

# 2. Find the end of HomeScreenContent before the next section
next_section_marker = "// COMPONENTE PRINCIPAL CON SafeAreaProvider"
idx_next = code.find(next_section_marker, idx_desktop)
if idx_next == -1:
    print("Error: Next section marker not found.")
    sys.exit(1)

# Find the last closing </View> before idx_next
idx_close_view = code.rfind("</View>", idx_desktop, idx_next)
if idx_close_view == -1:
    print("Error: Closing View not found.")
    sys.exit(1)

print(f"Indices: close_view={idx_close_view}, next={idx_next}")

# Verify closing block we are replacing
original_close_block = code[idx_close_view:idx_next]
print("--- MATCHED CLOSE BLOCK REPR ---")
print(repr(original_close_block))

# Define the new blocks (using flexible newlines/spaces)
# We preserve the double newlines or convert them to standard LF double newlines
# Let's replace the start block
new_start_block = """return (

    <View style={{ flex: 1, backgroundColor: bgMain, width: '100%', alignItems: 'center' }}>

      <View style={[

        styles.safeArea, 

        { paddingTop: insets.top, backgroundColor: bgMain, width: '100%' },

      """

# Let's replace the desktop style starting line to add borders
old_desktop_style = """isDesktopWeb ? {

        maxWidth: 485,"""

new_desktop_style = """isDesktopWeb ? {

        maxWidth: 485,

        borderLeftWidth: 1,

        borderRightWidth: 1,

        borderColor: borderCard,"""

# Let's replace the closing block
new_close_block = """</View>

      </View>

  );
}

"""

# Reconstruct code
part1 = code[:idx_return]
part2 = code[idx_return:idx_close_view]
part3 = code[idx_close_view:]

# Modify part2 (start block and desktop borders)
# We replace the exact slice `original_start_block` with `new_start_block`
part2 = part2.replace(original_start_block, new_start_block)

# Check and replace old_desktop_style in part2
old_desktop_style_norm = old_desktop_style.replace("\r\n", "\n")
if old_desktop_style_norm in part2:
    part2 = part2.replace(old_desktop_style_norm, new_desktop_style)
    print("Desktop premium borders added.")
else:
    # Try with double newlines
    old_desktop_style_double = """isDesktopWeb ? {\n\n\n\n\n\n\n        maxWidth: 485,"""
    new_desktop_style_double = """isDesktopWeb ? {\n\n\n\n\n\n\n        maxWidth: 485,\n\n\n\n\n\n\n        borderLeftWidth: 1,\n\n\n\n\n\n\n        borderRightWidth: 1,\n\n\n\n\n\n\n        borderColor: borderCard,"""
    if old_desktop_style_double in part2:
        part2 = part2.replace(old_desktop_style_double, new_desktop_style_double)
        print("Desktop premium borders added (double newlines).")
    else:
        print("Warning: Desktop style pattern not found. Proceeding without borders.")

# Modify part3 (closing block)
# We replace the exact slice `original_close_block` with our new wrapped closing tags
part3 = part3.replace(original_close_block, new_close_block)

final_code = part1 + part2 + part3

# Save
native_code = final_code.replace("\n", os.linesep)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(native_code)

print("DESKTOP THEME WRAPPING APPLIED AND SAVED SUCCESSFULLY!")
