import sys

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

targets = {}

targets["imports"] = """import { 
  View, Text, Image, ActivityIndicator, Alert, StyleSheet, 
  ScrollView, TouchableOpacity, Platform, StatusBar,
  Modal, TextInput, Dimensions, KeyboardAvoidingView, PanResponder,
  useWindowDimensions, TouchableWithoutFeedback, Linking
} from 'react-native';"""

targets["load_mode"] = """        const savedDarkMode = await AsyncStorage.getItem('@smart_pantry_dark_mode');
        if (savedDarkMode !== null) {
          setIsDarkMode(savedDarkMode === 'true');
        }"""

targets["toggle_function"] = """  const toggleDarkMode = async () => {
    const nextMode = !isDarkMode;
    setIsDarkMode(nextMode);
    try {
      await AsyncStorage.setItem('@smart_pantry_dark_mode', String(nextMode));
      addHistoryLog(`Tema cambiado a: ${nextMode ? 'Oscuro' : 'Claro'}`);
    } catch (e) {
      console.error("Error al guardar preferencia de modo oscuro:", e);
    }
  };"""

targets["derived_theme"] = """  const isDark = isDarkMode;
  const bgMain = isDark ? '#121212' : '#F7F9FB';
  const bgCard = isDark ? '#1E1E1E' : '#ffffff';
  const borderCard = isDark ? '#2D2D2D' : '#EBF1F6';
  const textPrimary = isDark ? '#F5F5F7' : '#1A1C1E';
  const textSecondary = isDark ? '#9CA3AF' : '#6B7280';
  const bgInput = isDark ? '#2A2A2A' : '#F3F4F6';"""

targets["settings_switch"] = """              {/* Interruptor Claro/Oscuro Profesional */}
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

targets["share_modal"] = """      {/* --- MODAL DE COMPARTIR CÓDIGO FAMILIAR (Modern Android Material You Dark-Theme Share Sheet) --- */}"""

targets["stylesheet_end"] = """  profileDetailValue: {
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

for name, target in targets.items():
    found = target in code
    print(f"Target '{name}': {'FOUND' if found else 'NOT FOUND'}")
    if not found:
        # Try to find a partial match or similar words
        first_line = target.strip().split('\n')[0]
        print(f"  Attempting to search for first line: '{first_line}'")
        idx = code.find(first_line)
        if idx != -1:
            print(f"  First line found at index {idx}! Showing context:")
            print(code[idx:idx+500])
        else:
            print(f"  First line NOT found either!")
