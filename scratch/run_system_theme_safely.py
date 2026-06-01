import os
import sys

# Configure stdout encoding to utf-8 if possible
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

if not os.path.exists(file_path):
    print("Error: HomeScreen.js not found.")
    sys.exit(1)

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# Normalize line endings to LF for internal processing
code = code.replace("\r\n", "\n")

# Replacements to perform
replacements = {}

# 1. Imports
old_imports = """import { 
  View, Text, Image, ActivityIndicator, Alert, StyleSheet, 
  ScrollView, TouchableOpacity, Platform, StatusBar,
  Modal, TextInput, Dimensions, KeyboardAvoidingView, PanResponder,
  useWindowDimensions, TouchableWithoutFeedback, Linking
} from 'react-native';"""

new_imports = """import { 
  View, Text, Image, ActivityIndicator, Alert, StyleSheet, 
  ScrollView, TouchableOpacity, Platform, StatusBar,
  Modal, TextInput, Dimensions, KeyboardAvoidingView, PanResponder,
  useWindowDimensions, TouchableWithoutFeedback, Linking, useColorScheme
} from 'react-native';"""

replacements["Imports"] = (old_imports, new_imports)

# 2. State hooks
replacements["State hook"] = (
    "const [isDarkMode, setIsDarkMode] = useState(false);",
    "const [themeMode, setThemeMode] = useState('system'); // 'light' | 'dark' | 'system'"
)

# 3. useEffect loadLocalProfile
old_load_mode = """        const savedDarkMode = await AsyncStorage.getItem('@smart_pantry_dark_mode');
        if (savedDarkMode !== null) {
          setIsDarkMode(savedDarkMode === 'true');
        }"""

new_load_mode = """        const savedThemeMode = await AsyncStorage.getItem('@smart_pantry_theme_mode');
        if (savedThemeMode !== null) {
          setThemeMode(savedThemeMode);
        } else {
          const savedDarkMode = await AsyncStorage.getItem('@smart_pantry_dark_mode');
          if (savedDarkMode !== null) {
            setThemeMode(savedDarkMode === 'true' ? 'dark' : 'light');
          }
        }"""

replacements["AsyncStorage load"] = (old_load_mode, new_load_mode)

# 4. toggleDarkMode function
old_toggle_function = """  const toggleDarkMode = async () => {
    const nextMode = !isDarkMode;
    setIsDarkMode(nextMode);
    try {
      await AsyncStorage.setItem('@smart_pantry_dark_mode', String(nextMode));
      addHistoryLog(`Tema cambiado a: ${nextMode ? 'Oscuro' : 'Claro'}`);
    } catch (e) {
      console.error("Error al guardar preferencia de modo oscuro:", e);
    }
  };"""

new_toggle_function = """  const changeThemeMode = async (mode) => {
    setThemeMode(mode);
    try {
      await AsyncStorage.setItem('@smart_pantry_theme_mode', mode);
      addHistoryLog(`Preferencia de tema actualizada a: ${mode}`);
    } catch (e) {
      console.error("Error al guardar preferencia de tema:", e);
    }
  };"""

replacements["toggleDarkMode function"] = (old_toggle_function, new_toggle_function)

# 5. Derived theme variables
old_derived_theme = """  const isDark = isDarkMode;
  const bgMain = isDark ? '#121212' : '#F7F9FB';
  const bgCard = isDark ? '#1E1E1E' : '#ffffff';
  const borderCard = isDark ? '#2D2D2D' : '#EBF1F6';
  const textPrimary = isDark ? '#F5F5F7' : '#1A1C1E';
  const textSecondary = isDark ? '#9CA3AF' : '#6B7280';
  const bgInput = isDark ? '#2A2A2A' : '#F3F4F6';"""

new_derived_theme = """  const systemScheme = useColorScheme();
  const isDark = themeMode === 'system' ? (systemScheme === 'dark') : (themeMode === 'dark');
  const isDarkMode = isDark; // compatibility
  const bgMain = isDark ? '#121212' : '#F7F9FB';
  const bgCard = isDark ? '#1E1E1E' : '#ffffff';
  const borderCard = isDark ? '#2D2D2D' : '#EBF1F6';
  const textPrimary = isDark ? '#F5F5F7' : '#1A1C1E';
  const textSecondary = isDark ? '#9CA3AF' : '#6B7280';
  const bgInput = isDark ? '#2A2A2A' : '#F3F4F6';"""

replacements["Derived theme variables"] = (old_derived_theme, new_derived_theme)

# 6. Settings switch
old_settings_switch = """              {/* Interruptor Claro/Oscuro Profesional */}
              <View style={[styles.settingRow, { borderBottomColor: isDark ? '#2D2D2D' : '#F3F4F6' }]}>
                <View style={styles.settingRowLeft}>
                  <Ionicons name={isDarkMode ? "moon" : "sunny"} size={24} color={isDarkMode ? themeColor : "#1F2937"} />
                  <Text style={[styles.settingRowText, { color: textPrimary }]}>Modo Oscuro</Text>
                </View>
                <TouchableOpacity 
                  style={[
                    styles.themeSwitchContainer, 
                    { backgroundColor: isDarkMode ? themeColor : '#E2E8F0' }
                  ]}
                  onPress={toggleDarkMode}
                >
                  <View style={[
                    styles.themeSwitchCircle, 
                    { transform: [{ translateX: isDarkMode ? 20 : 0 }] }
                  ]} />
                </TouchableOpacity>
              </View>"""

new_settings_switch = """              {/* Selector de Tema Claro/Oscuro/Sistema Profesional */}
              <View style={[styles.settingRow, { borderBottomColor: isDark ? '#2D2D2D' : '#F3F4F6', flexDirection: 'column', alignItems: 'stretch', gap: 10 }]}>
                <View style={{ flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', width: '100%' }}>
                  <View style={styles.settingRowLeft}>
                    <Ionicons name={isDark ? "moon" : "sunny"} size={24} color={isDark ? themeColor : "#1F2937"} />
                    <Text style={[styles.settingRowText, { color: textPrimary }]}>Tema de Pantalla</Text>
                  </View>
                  <Text style={{ fontSize: 12, fontWeight: '700', color: themeColor }}>
                    {themeMode === 'system' ? 'Sistema' : themeMode === 'dark' ? 'Oscuro' : 'Claro'}
                  </Text>
                </View>
                <View style={styles.themeModePillsRow}>
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
                </View>
              </View>"""

replacements["Settings switch"] = (old_settings_switch, new_settings_switch)

# 8. Stylesheet end
old_stylesheet_end_actual = """  profileDetailValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
  },
  themeSwitchContainer: {
    width: 46,
    height: 26,
    borderRadius: 13,
    padding: 3,
    justifyContent: 'center',
  },
  themeSwitchCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 2.5,
    elevation: 2,
  }
});"""

new_stylesheet_end = """  profileDetailValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
  },
  themeSwitchContainer: {
    width: 46,
    height: 26,
    borderRadius: 13,
    padding: 3,
    justifyContent: 'center',
  },
  themeSwitchCircle: {
    width: 20,
    height: 20,
    borderRadius: 10,
    backgroundColor: '#ffffff',
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 2.5,
    elevation: 2,
  },
  themeModePillsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    width: '100%',
    gap: 8,
    marginTop: 4,
  },
  themeModePill: {
    flex: 1,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    gap: 6,
    paddingVertical: 10,
    borderRadius: 12,
    backgroundColor: '#F1F5F9',
    borderWidth: 1.5,
    borderColor: 'transparent',
  },
  themeModePillActive: {
    borderWidth: 1.5,
    borderColor: '#ffffff',
  },
  themeModePillText: {
    fontSize: 12.5,
    fontWeight: '700',
  },
  themeModePillTextActive: {
    fontWeight: '800',
  }
});"""

replacements["Stylesheet end"] = (old_stylesheet_end_actual, new_stylesheet_end)

# Apply normal string replacements
all_ok = True
for name, (old, new) in replacements.items():
    old_norm = old.replace("\r\n", "\n")
    if old_norm not in code:
        print(f"Error: Target '{name}' not found exactly in HomeScreen.js.")
        all_ok = False
    else:
        code = code.replace(old_norm, new.replace("\r\n", "\n"))
        print(f"Success: Target '{name}' replaced in-memory.")

# Dynamic replacement for the Share Modal boundary
start_marker = "{/* --- MODAL DE COMPARTIR CÓDIGO FAMILIAR"
idx = code.find(start_marker)
if idx == -1:
    print("Error: Share modal start marker not found.")
    all_ok = False
else:
    end_marker = "</ModalWrapper>"
    end_idx = code.find(end_marker, idx)
    if end_idx == -1:
        print("Error: Share modal end marker not found after start marker.")
        all_ok = False
    else:
        # We replace from index `idx` to `end_idx + len(end_marker)`
        new_share_modal_jsx = """      {/* --- MODAL DE COMPARTIR CÓDIGO FAMILIAR (Modern Android Material You Dark-Theme Share Sheet) --- */}
      <ModalWrapper visible={showShareModal} animationType="slide" transparent={true} onRequestClose={() => setShowShareModal(false)}>
        <TouchableOpacity 
          style={[styles.shareOverlayAndroid, { backgroundColor: isDark ? 'rgba(0,0,0,0.7)' : 'rgba(15, 23, 42, 0.4)' }]} 
          activeOpacity={1} 
          onPress={() => setShowShareModal(false)}
        >
          <View style={[styles.shareSheetMainAndroid, { backgroundColor: bgCard, borderColor: borderCard }]} {...sharePanResponder.panHandlers}>
            <View style={[styles.shareSheetHandleAndroid, { backgroundColor: isDark ? '#4E463D' : '#E2E8F0' }]} />
            
            {/* Title */}
            <Text style={[styles.shareSheetTitleAndroid, { color: textPrimary }]}>Compartir Código</Text>
            
            {/* Preview Card */}
            <View style={[styles.sharePreviewCardAndroid, { backgroundColor: isDark ? '#2D231E' : '#F8FAFC', borderColor: isDark ? '#4E3E35' : '#E2E8F0' }]}>
              <View style={[styles.sharePreviewIconBox, { backgroundColor: themeColor }]}>
                <Ionicons name="people" size={24} color="#fff" />
              </View>
              <View style={styles.sharePreviewTextColumn}>
                <Text style={[styles.sharePreviewTitle, { color: textPrimary }]}>Despensa Familiar SmartPantry</Text>
                <Text style={[styles.sharePreviewSubtitle, { color: textSecondary }]}>Código: {userProfile.familyCode}</Text>
              </View>
            </View>
            
            {/* Row 1: Contactos Frecuentes */}
            <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.shareContactsScrollAndroid}>
              {/* GP MOBILE */}
              <TouchableOpacity style={styles.shareContactItemAndroid} onPress={copyFamilyCode}>
                <View style={styles.shareContactAvatarWrapperAndroid}>
                  <View style={[styles.shareContactAvatarAndroid, { backgroundColor: '#1A5F35', borderColor: isDark ? '#3D3530' : '#E2E8F0' }]}>
                    <Ionicons name="volume-high" size={22} color="#fff" />
                  </View>
                  <View style={[styles.shareContactBadgeAndroid, { backgroundColor: '#25D366', borderColor: bgCard }]}>
                    <Ionicons name="logo-whatsapp" size={10} color="#fff" />
                  </View>
                </View>
                <Text style={[styles.shareContactNameAndroid, { color: textSecondary }]} numberOfLines={2}>GP MOBILE</Text>
              </TouchableOpacity>

              {/* La Familia */}
              <TouchableOpacity style={styles.shareContactItemAndroid} onPress={copyFamilyCode}>
                <View style={styles.shareContactAvatarWrapperAndroid}>
                  <View style={[styles.shareContactAvatarAndroid, { backgroundColor: '#B04E36', borderColor: isDark ? '#3D3530' : '#E2E8F0' }]}>
                    <Ionicons name="people" size={22} color="#fff" />
                  </View>
                  <View style={[styles.shareContactBadgeAndroid, { backgroundColor: '#25D366', borderColor: bgCard }]}>
                    <Ionicons name="logo-whatsapp" size={10} color="#fff" />
                  </View>
                </View>
                <Text style={[styles.shareContactNameAndroid, { color: textSecondary }]} numberOfLines={2}>La Familia 😍</Text>
              </TouchableOpacity>

              {/* Tío Siete */}
              <TouchableOpacity style={styles.shareContactItemAndroid} onPress={copyFamilyCode}>
                <View style={styles.shareContactAvatarWrapperAndroid}>
                  <View style={[styles.shareContactAvatarAndroid, { backgroundColor: '#473680', borderColor: isDark ? '#3D3530' : '#E2E8F0' }]}>
                    <Text style={{ color: '#fff', fontSize: 13, fontWeight: '800' }}>TÍO</Text>
                  </View>
                  <View style={[styles.shareContactBadgeAndroid, { backgroundColor: '#25D366', borderColor: bgCard }]}>
                    <Ionicons name="logo-whatsapp" size={10} color="#fff" />
                  </View>
                </View>
                <Text style={[styles.shareContactNameAndroid, { color: textSecondary }]} numberOfLines={2}>Tío Siete</Text>
              </TouchableOpacity>

              {/* Nando Abuelo */}
              <TouchableOpacity style={styles.shareContactItemAndroid} onPress={copyFamilyCode}>
                <View style={styles.shareContactAvatarWrapperAndroid}>
                  <View style={[styles.shareContactAvatarAndroid, { backgroundColor: '#1A4F7C', borderColor: isDark ? '#3D3530' : '#E2E8F0' }]}>
                    <Text style={{ color: '#fff', fontSize: 14, fontWeight: '800' }}>NA</Text>
                  </View>
                  <View style={[styles.shareContactBadgeAndroid, { backgroundColor: '#007AFF', borderColor: bgCard }]}>
                    <Ionicons name="chatbubble" size={9} color="#fff" />
                  </View>
                </View>
                <Text style={[styles.shareContactNameAndroid, { color: textSecondary }]} numberOfLines={2}>Nando Abuelo</Text>
              </TouchableOpacity>

              {/* Nota Personal */}
              <TouchableOpacity style={styles.shareContactItemAndroid} onPress={copyFamilyCode}>
                <View style={styles.shareContactAvatarWrapperAndroid}>
                  <View style={[styles.shareContactAvatarAndroid, { backgroundColor: '#64748B', borderColor: isDark ? '#3D3530' : '#E2E8F0' }]}>
                    <Ionicons name="document-text" size={22} color="#fff" />
                  </View>
                  <View style={[styles.shareContactBadgeAndroid, { backgroundColor: '#007AFF', borderColor: bgCard }]}>
                    <Ionicons name="chatbubble" size={9} color="#fff" />
                  </View>
                </View>
                <Text style={[styles.shareContactNameAndroid, { color: textSecondary }]} numberOfLines={2}>Nota personal</Text>
              </TouchableOpacity>
            </ScrollView>
            
            <View style={[styles.shareDividerAndroid, { backgroundColor: isDark ? '#352F30' : '#E2E8F0' }]} />

            {/* Row 2: Grid de Aplicaciones */}
            <View style={styles.shareAppsGridAndroid}>
              {/* Quick Share */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={copyFamilyCode}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#0A84FF' }]}>
                  <Ionicons name="swap-horizontal" size={26} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Quick Share</Text>
              </TouchableOpacity>

              {/* WhatsApp */}
              <TouchableOpacity 
                style={styles.shareAppItemAndroid} 
                onPress={async () => {
                  const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(`¡Hola! Únete a mi despensa familiar en SmartPantry. Usa este código de sincronización: ${userProfile.familyCode}`)}`;
                  Platform.OS === 'web' ? window.open(url, '_blank') : await Linking.openURL(url);
                }}
              >
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#30D158' }]}>
                  <Ionicons name="logo-whatsapp" size={28} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>WhatsApp</Text>
              </TouchableOpacity>

              {/* Telegram */}
              <TouchableOpacity 
                style={styles.shareAppItemAndroid} 
                onPress={async () => {
                  const url = `https://t.me/share/url?url=${encodeURIComponent('https://smartpantry.com')}&text=${encodeURIComponent(`¡Hola! Únete a mi despensa familiar en SmartPantry. Usa este código de sincronización: ${userProfile.familyCode}`)}`;
                  Platform.OS === 'web' ? window.open(url, '_blank') : await Linking.openURL(url);
                }}
              >
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#5856D6' }]}>
                  <Ionicons name="paper-plane" size={24} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Telegram</Text>
              </TouchableOpacity>

              {/* Gemini */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={copyFamilyCode}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: isDark ? '#F2F2F7' : '#F1F5F9', borderWidth: 1.5, borderColor: isDark ? '#D1D1D6' : '#E2E8F0' }]}>
                  <Ionicons name="sparkles" size={24} color="#34C759" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Gemini</Text>
              </TouchableOpacity>

              {/* DeepSeek */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={copyFamilyCode}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#0F172A' }]}>
                  <Ionicons name="navigate" size={24} color="#38BDF8" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>DeepSeek</Text>
              </TouchableOpacity>
            </View>

            <View style={styles.shareAppsGridAndroid}>
              {/* Copiar Código */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={copyFamilyCode}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: isDark ? '#3A3A3C' : '#F1F5F9', borderWidth: 1.5, borderColor: isDark ? '#4E4E4E' : '#E2E8F0' }]}>
                  <Ionicons name="copy" size={24} color={isDark ? "#fff" : "#475569"} />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Copiar</Text>
              </TouchableOpacity>

              {/* Gmail */}
              <TouchableOpacity 
                style={styles.shareAppItemAndroid}
                onPress={async () => {
                  const url = `mailto:?subject=${encodeURIComponent('Únete a mi despensa familiar en SmartPantry')}&body=${encodeURIComponent(`¡Hola! Únete a mi despensa familiar en SmartPantry. Usa este código de sincronización: ${userProfile.familyCode}`)}`;
                  Platform.OS === 'web' ? window.open(url, '_blank') : await Linking.openURL(url);
                }}
              >
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#FF453A' }]}>
                  <Ionicons name="mail" size={24} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Gmail</Text>
              </TouchableOpacity>

              {/* Discord */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={copyFamilyCode}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#5865F2' }]}>
                  <Ionicons name="logo-discord" size={24} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Discord</Text>
              </TouchableOpacity>

              {/* Regenerar */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={() => {
                setShowShareModal(false);
                generateFamilyCode();
              }}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: isDark ? '#636366' : '#F1F5F9', borderWidth: 1.5, borderColor: isDark ? '#4E4E4E' : '#E2E8F0' }]}>
                  <Ionicons name="refresh" size={24} color={isDark ? "#fff" : "#475569"} />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Regenerar</Text>
              </TouchableOpacity>

              {/* Cerrar */}
              <TouchableOpacity style={styles.shareAppItemAndroid} onPress={() => setShowShareModal(false)}>
                <View style={[styles.shareAppIconBoxAndroid, { backgroundColor: '#FF3B30' }]}>
                  <Ionicons name="close" size={24} color="#fff" />
                </View>
                <Text style={[styles.shareAppNameAndroid, { color: textSecondary }]}>Cerrar</Text>
              </TouchableOpacity>
            </View>
          </View>
        </TouchableOpacity>
      </ModalWrapper>"""
        
        # Replace the range
        part1 = code[:idx]
        part2 = code[end_idx + len(end_marker):]
        code = part1 + new_share_modal_jsx + part2
        print("Success: Share modal boundary replaced successfully.")

# Write changes back if all_ok
if all_ok:
    # Use native platform line endings when saving
    native_code = code.replace("\n", os.linesep)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(native_code)
    print("ALL CHANGES SAVED SUCCESSFULLY TO HOMESCREEN.JS!")
else:
    print("ABORTED: Replacement verification failed. File NOT modified.")
