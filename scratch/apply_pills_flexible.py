import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

# Find the start of the themeModePillsRow View
start_marker = "style={styles.themeModePillsRow}"
start_idx = code.find(start_marker)
if start_idx == -1:
    # Try with double spaces or other variations
    start_marker = "style={styles.themeModePillsRow}"
    print("Error: Pills row start marker not found.")
    sys.exit(1)

print("Found start marker at index", start_idx)

# Find the closing </View> after this start_idx
# The View contains three TouchableOpacity buttons and their children.
# So we want to find the closing </View> that matches the row container.
# Since it is a ScrollView and has no nested Views inside the PillsRow container,
# the next </View> is exactly the closing tag of the pills row container!
end_marker = "</View>"
end_idx = code.find(end_marker, start_idx)
if end_idx == -1:
    print("Error: Closing View tag not found.")
    sys.exit(1)

print("Found closing View tag at index", end_idx)

# Let's slice the code to be absolutely sure what we are replacing
pills_block = code[start_idx : end_idx + len(end_marker)]
print("--- ACTUAL PILLS BLOCK START ---")
print(pills_block[:300])
print("...")
print(pills_block[-100:])
print("--- ACTUAL PILLS BLOCK END ---")

# Replace this exact block with our new premium dynamic pills row
new_pills_block = """style={styles.themeModePillsRow}>

                  <TouchableOpacity 
                    style={[styles.themeModePill, { backgroundColor: isDark ? '#242424' : '#F1F5F9', borderColor: isDark ? '#3D3D3D' : 'transparent' }, themeMode === 'light' && { backgroundColor: themeColor, borderColor: themeColor }]}
                    onPress={() => changeThemeMode('light')}
                  >
                    <Ionicons name="sunny-outline" size={16} color={themeMode === 'light' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'light' && styles.themeModePillTextActive, { color: themeMode === 'light' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Claro</Text>
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.themeModePill, { backgroundColor: isDark ? '#242424' : '#F1F5F9', borderColor: isDark ? '#3D3D3D' : 'transparent' }, themeMode === 'dark' && { backgroundColor: themeColor, borderColor: themeColor }]}
                    onPress={() => changeThemeMode('dark')}
                  >
                    <Ionicons name="moon-outline" size={16} color={themeMode === 'dark' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'dark' && styles.themeModePillTextActive, { color: themeMode === 'dark' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Oscuro</Text>
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.themeModePill, { backgroundColor: isDark ? '#242424' : '#F1F5F9', borderColor: isDark ? '#3D3D3D' : 'transparent' }, themeMode === 'system' && { backgroundColor: themeColor, borderColor: themeColor }]}
                    onPress={() => changeThemeMode('system')}
                  >
                    <Ionicons name="options-outline" size={16} color={themeMode === 'system' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'system' && styles.themeModePillTextActive, { color: themeMode === 'system' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Sistema</Text>
                  </TouchableOpacity>
                </View>"""

# Replace the block
code = code[:start_idx] + new_pills_block + code[end_idx + len(end_marker):]

# Also ensure scroll padding is updated if not already
old_padding = "  const scrollPaddingBottom = bottomNavHeight + 40;"
new_padding = "  const scrollPaddingBottom = bottomNavHeight + 110;"
if old_padding in code:
    code = code.replace(old_padding, new_padding)
    print("Scroll padding bottom updated.")
else:
    print("Scroll padding bottom was already updated or not found.")

native_code = code.replace("\n", os.linesep)
with open(file_path, "w", encoding="utf-8") as f:
    f.write(native_code)

print("PILLS AND SCROLL UX REPLACED AND SAVED SUCCESSFULLY!")
