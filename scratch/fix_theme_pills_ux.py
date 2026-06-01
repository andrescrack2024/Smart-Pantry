import os
import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

code = code.replace("\r\n", "\n")

replacements = []

# 1. Update scrollPaddingBottom to give extra padding so content clears the camera FAB
old_padding = "  const scrollPaddingBottom = bottomNavHeight + 40;"
new_padding = "  const scrollPaddingBottom = bottomNavHeight + 110;"
replacements.append(("Scroll padding bottom", old_padding, new_padding))

# 2. Update the theme mode pills row JSX to be fully dynamic
old_pills_row = """                <View style={styles.themeModePillsRow}>
                  <TouchableOpacity 
                    style={[styles.themeModePill, themeMode === 'light' && { backgroundColor: themeColor }]}
                    onPress={() => changeThemeMode('light')}
                  >
                    <Ionicons name="sunny-outline" size={16} color={themeMode === 'light' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'light' && styles.themeModePillTextActive, { color: themeMode === 'light' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Claro</Text>
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.themeModePill, themeMode === 'dark' && { backgroundColor: themeColor }]}
                    onPress={() => changeThemeMode('dark')}
                  >
                    <Ionicons name="moon-outline" size={16} color={themeMode === 'dark' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'dark' && styles.themeModePillTextActive, { color: themeMode === 'dark' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Oscuro</Text>
                  </TouchableOpacity>

                  <TouchableOpacity 
                    style={[styles.themeModePill, themeMode === 'system' && { backgroundColor: themeColor }]}
                    onPress={() => changeThemeMode('system')}
                  >
                    <Ionicons name="options-outline" size={16} color={themeMode === 'system' ? '#fff' : (isDark ? '#aaa' : '#444')} />
                    <Text style={[styles.themeModePillText, themeMode === 'system' && styles.themeModePillTextActive, { color: themeMode === 'system' ? '#fff' : (isDark ? '#CAC4D0' : '#475569') }]}>Sistema</Text>
                  </TouchableOpacity>
                </View>"""

new_pills_row = """                <View style={styles.themeModePillsRow}>
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

replacements.append(("Theme pills row", old_pills_row, new_pills_row))

all_ok = True
for name, old, new in replacements:
    old_norm = old.replace("\r\n", "\n")
    if old_norm not in code:
        print(f"Error: Target '{name}' not found exactly.")
        all_ok = False
    else:
        code = code.replace(old_norm, new.replace("\r\n", "\n"))
        print(f"Success: Target '{name}' replaced.")

if all_ok:
    native_code = code.replace("\n", os.linesep)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(native_code)
    print("ALL THEME PILLS AND SCROLL UX FIXES APPLIED SUCCESSFULLY!")
else:
    print("ABORTED: Theme pills UX fixes could not be applied.")
