import re

file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

# 1. Update InputField definition to accept style overrides or adapt to theme
old_input_field = """const InputField = ({ placeholder, value, onChangeText, error, onClearError, ...props }) => (
  <View style={{ marginBottom: 14 }}>
    <TextInput 
      style={[styles.input, error && styles.inputError]} 
      placeholder={placeholder} 
      value={value} 
      onChangeText={(text) => {
        onChangeText(text);
        if (error && onClearError) onClearError();
      }}
      placeholderTextColor="#999"
      {...props} 
    />
    {error && <Text style={styles.fieldErrorText}>{error}</Text>}
  </View>
);"""

new_input_field = """const InputField = ({ placeholder, value, onChangeText, error, onClearError, style, ...props }) => (
  <View style={{ marginBottom: 14 }}>
    <TextInput 
      style={[styles.input, error && styles.inputError, style]} 
      placeholder={placeholder} 
      value={value} 
      onChangeText={(text) => {
        onChangeText(text);
        if (error && onClearError) onClearError();
      }}
      placeholderTextColor="#999"
      {...props} 
    />
    {error && <Text style={styles.fieldErrorText}>{error}</Text>}
  </View>
);"""

code = code.replace(old_input_field, new_input_field)

# 2. Add the dynamic switch toggle under Personalization in activeTab === 'perfil'
old_theme_section = """              {/* PERSONALIZACIÓN */}
              <Text style={styles.settingGroupHeader}>PERSONALIZACIÓN</Text>
              <Text style={styles.settingLabelText}>Tema de Color:</Text>
              <View style={styles.themeSelectorRow}>"""

new_theme_section = """              {/* PERSONALIZACIÓN */}
              <Text style={[styles.settingGroupHeader, { color: textPrimary }]}>PERSONALIZACIÓN</Text>
              
              {/* Interruptor Claro/Oscuro Profesional */}
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
              </View>

              <Text style={[styles.settingLabelText, { color: textSecondary }]}>Tema de Color:</Text>
              <View style={styles.themeSelectorRow}>"""

code = code.replace(old_theme_section, new_theme_section)

# 3. Add themeSwitchContainer and themeSwitchCircle styles to the StyleSheet
old_stylesheet_end = """  socialBtnFacebookText: {
    fontSize: 14,
    color: '#ffffff',
    fontWeight: '700',
  }
});"""

# Note: We added profileDetailsCard styles in previous step, so let's target the exact end of StyleSheet
old_stylesheet_end_actual = """  profileDetailValue: {
    fontSize: 14,
    fontWeight: '700',
    color: '#0F172A',
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
  }
});"""

code = code.replace(old_stylesheet_end_actual, new_stylesheet_end)

# 4. Modify main containers
code = code.replace("styles.safeArea, \n      { paddingTop: insets.top },", "styles.safeArea, \n      { paddingTop: insets.top, backgroundColor: bgMain },")
code = code.replace("styles.safeArea, \r\n      { paddingTop: insets.top },", "styles.safeArea, \r\n      { paddingTop: insets.top, backgroundColor: bgMain },")

code = code.replace('<StatusBar barStyle="dark-content" backgroundColor="#F7F9FB" />', 
                    '<StatusBar barStyle={isDark ? "light-content" : "dark-content"} backgroundColor={bgMain} />')

code = code.replace("<Text style={{ fontSize: 24, fontWeight: '900', color: '#1A1C1E', letterSpacing: -0.5 }}>SmartPantry</Text>",
                    "<Text style={{ fontSize: 24, fontWeight: '900', color: textPrimary, letterSpacing: -0.5 }}>SmartPantry</Text>")

# 5. Header location container
code = code.replace("style={styles.locationContainer}", "style={[styles.locationContainer, { backgroundColor: bgCard }]}")
code = code.replace("style={styles.locationText}", "style={[styles.locationText, { color: textSecondary }]}")

# 6. Search bar
code = code.replace("style={styles.searchBar}", "style={[styles.searchBar, { backgroundColor: bgCard, borderColor: borderCard }]}")
code = code.replace("style={styles.searchText}", "style={[styles.searchText, { color: textSecondary }]}")

# 7. Category selector
code = code.replace("styles.categoryIcon, \n                    activeCategory === cat && { backgroundColor: themeColor, shadowColor: themeColor }",
                    "styles.categoryIcon, { backgroundColor: bgCard }, \n                    activeCategory === cat && { backgroundColor: themeColor, shadowColor: themeColor }")
code = code.replace("styles.categoryIcon, \r\n                    activeCategory === cat && { backgroundColor: themeColor, shadowColor: themeColor }",
                    "styles.categoryIcon, { backgroundColor: bgCard }, \n                    activeCategory === cat && { backgroundColor: themeColor, shadowColor: themeColor }")

code = code.replace('color={activeCategory === cat ? "#fff" : "#444"}',
                    'color={activeCategory === cat ? "#fff" : (isDark ? "#CAC4D0" : "#444")}')

code = code.replace("style={[styles.categoryText, activeCategory === cat && { color: themeColor, fontWeight: '800' }]}",
                    "style={[styles.categoryText, { color: textSecondary }, activeCategory === cat && { color: themeColor, fontWeight: '800' }]}")

# 8. Section titles
code = code.replace("style={styles.sectionTitle}", "style={[styles.sectionTitle, { color: textPrimary }]}")
code = code.replace("style={styles.sectionSubtitleText}", "style={[styles.sectionSubtitleText, { color: textSecondary }]}")

# 9. Product Card
code = code.replace("style={styles.card}", "style={[styles.card, { backgroundColor: bgCard, borderColor: borderCard }]}")
code = code.replace("style={styles.cardTitle}", "style={[styles.cardTitle, { color: textPrimary }]}")
code = code.replace("style={styles.cardImageContainer}", "style={[styles.cardImageContainer, { backgroundColor: isDark ? '#242424' : '#F8FAFC' }]}")
code = code.replace("style={styles.freshnessBarBg}", "style={[styles.freshnessBarBg, { backgroundColor: isDark ? '#333333' : '#F1F3F5' }]}")

# 10. Settings Page Card (Profile)
code = code.replace("style={styles.settingCard}", "style={[styles.settingCard, { backgroundColor: bgCard, borderColor: borderCard }]}")
code = code.replace("style={styles.settingGroupHeader}", "style={[styles.settingGroupHeader, { color: textPrimary }]}")
code = code.replace("style={styles.settingRow}", "style={[styles.settingRow, { borderBottomColor: isDark ? '#2D2D2D' : '#F3F4F6' }]}")
code = code.replace("style={styles.settingRowText}", "style={[styles.settingRowText, { color: textPrimary }]}")
code = code.replace('color="#1F2937"', 'color={isDark ? themeColor : "#1F2937"}')
code = code.replace("style={styles.settingLabelText}", "style={[styles.settingLabelText, { color: textSecondary }]}")
code = code.replace("style={styles.familyCodeDisplayBlock}", "style={[styles.familyCodeDisplayBlock, { backgroundColor: isDark ? '#2A2A2A' : '#F3F4F6' }]}")
code = code.replace("style={styles.familyCodeTextVal}", "style={[styles.familyCodeTextVal, { color: textPrimary }]}")
code = code.replace("style={styles.familyCodeActionText}", "style={[styles.familyCodeActionText, { color: textSecondary }]}")
code = code.replace("style={styles.joinInputText}", "style={[styles.joinInputText, { backgroundColor: isDark ? '#242424' : '#F9FAFB', borderColor: isDark ? '#3D3D3D' : '#D1D5DB', color: textPrimary }]}")
code = code.replace("style={styles.joinSubmitBtn}", "style={[styles.joinSubmitBtn, { backgroundColor: isDark ? themeColor : '#111827' }]}")

# 11. Profile Header Name Section
code = code.replace("style={styles.profileNameText}", "style={[styles.profileNameText, { color: textPrimary }]}")
code = code.replace("style={styles.profileEmailText}", "style={[styles.profileEmailText, { color: textSecondary }]}")
code = code.replace("style={styles.avatarPlaceholder}", "style={[styles.avatarPlaceholder, { backgroundColor: isDark ? '#2D2D2D' : '#EAEFF3', borderColor: bgMain }]}")
code = code.replace("style={styles.avatarImage}", "style={[styles.avatarImage, { borderColor: bgMain }]}")
code = code.replace("style={styles.profileHeaderBg}", "style={[styles.profileHeaderBg, { backgroundColor: isDark ? '#1C1B1F' : '#E5E7EB' }]}")

# 12. Bottom Navigation
code = code.replace("style={styles.bottomNav}", "style={[styles.bottomNav, { backgroundColor: bgCard, borderTopColor: isDark ? '#2D2D2D' : '#EEF2F6' }]}")
code = code.replace("color={activeTab === 'inicio' ? themeColor : \"#a2a2a2\"}", "color={activeTab === 'inicio' ? themeColor : (isDark ? '#8A8A8A' : '#a2a2a2')}")
code = code.replace("color={activeTab === 'favoritos' ? themeColor : \"#a2a2a2\"}", "color={activeTab === 'favoritos' ? themeColor : (isDark ? '#8A8A8A' : '#a2a2a2')}")
code = code.replace("color={activeTab === 'historial' ? themeColor : \"#a2a2a2\"}", "color={activeTab === 'historial' ? themeColor : (isDark ? '#8A8A8A' : '#a2a2a2')}")
code = code.replace("color={activeTab === 'perfil' ? themeColor : \"#a2a2a2\"}", "color={activeTab === 'perfil' ? themeColor : (isDark ? '#8A8A8A' : '#a2a2a2')}")

code = code.replace("style={[styles.navText, activeTab === 'inicio' && { color: themeColor, fontWeight: '700' }]}",
                    "style={[styles.navText, { color: textSecondary }, activeTab === 'inicio' && { color: themeColor, fontWeight: '700' }]}")
code = code.replace("style={[styles.navText, activeTab === 'favoritos' && { color: themeColor, fontWeight: '700' }]}",
                    "style={[styles.navText, { color: textSecondary }, activeTab === 'favoritos' && { color: themeColor, fontWeight: '700' }]}")
code = code.replace("style={[styles.navText, activeTab === 'historial' && { color: themeColor, fontWeight: '700' }]}",
                    "style={[styles.navText, { color: textSecondary }, activeTab === 'historial' && { color: themeColor, fontWeight: '700' }]}")
code = code.replace("style={[styles.navText, activeTab === 'perfil' && { color: themeColor, fontWeight: '700' }]}",
                    "style={[styles.navText, { color: textSecondary }, activeTab === 'perfil' && { color: themeColor, fontWeight: '700' }]}")

# 13. InputFields theme in Auth Modal
code = code.replace('placeholder="Nombre de Usuario"', 'style={{ backgroundColor: bgInput, color: textPrimary }} placeholder="Nombre de Usuario"')
code = code.replace('placeholder="Correo o Teléfono (ej: +573123456789)"', 'style={{ backgroundColor: bgInput, color: textPrimary }} placeholder="Correo o Teléfono (ej: +573123456789)"')
code = code.replace('style={styles.passwordContainer}', 'style={[styles.passwordContainer, { backgroundColor: bgInput }]}')
code = code.replace('style={styles.passwordInput}', 'style={[styles.passwordInput, { color: textPrimary }]}')

# 14. Modals content backgrounds
code = code.replace("style={styles.modalContent}", "style={[styles.modalContent, { backgroundColor: bgCard }]}")
code = code.replace("style={[styles.modalContent, { paddingBottom: 40 }]}", "style={[styles.modalContent, { paddingBottom: 40, backgroundColor: bgCard }]}")
code = code.replace("style={[styles.modalContent, { paddingBottom: 30, maxHeight: height * 0.9 }]}", "style={[styles.modalContent, { paddingBottom: 30, maxHeight: height * 0.9, backgroundColor: bgCard }]}")
code = code.replace("style={styles.modalTitle}", "style={[styles.modalTitle, { color: textPrimary }]}")
code = code.replace("style={styles.modalSubtitle}", "style={[styles.modalSubtitle, { color: textSecondary }]}")
code = code.replace("style={styles.modalHandle}", "style={[styles.modalHandle, { backgroundColor: isDark ? '#4E4E4E' : '#E5E7EB' }]}")

# 15. Detail Editor Modal specifics
code = code.replace("style={styles.detailNameInput}", "style={[styles.detailNameInput, { color: textPrimary, borderBottomColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}")
code = code.replace("style={styles.quantityEditorContainer}", "style={[styles.quantityEditorContainer, { backgroundColor: isDark ? '#242424' : '#F8FAFC', borderColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}")
code = code.replace("style={styles.quantityEditorLabel}", "style={[styles.quantityEditorLabel, { color: textSecondary }]}")
code = code.replace("style={styles.qtyValueText}", "style={[styles.qtyValueText, { color: textPrimary }]}")
code = code.replace("style={styles.qtyBtn}", "style={[styles.qtyBtn, { backgroundColor: isDark ? '#2A2A2A' : '#ffffff', borderColor: isDark ? '#3D3D3D' : themeColor }]}")
code = code.replace("style={styles.aiTipContainer}", "style={[styles.aiTipContainer, { backgroundColor: isDark ? '#2A2518' : '#FFFDE7', borderLeftColor: '#FBC02D' }]}")
code = code.replace("style={styles.aiTipText}", "style={[styles.aiTipText, { color: isDark ? '#D9C5B2' : '#5D4037' }]}")

# 16. Profile Details Card Modal specifics
code = code.replace("style={styles.profileDetailsCard}", "style={[styles.profileDetailsCard, { backgroundColor: isDark ? '#242424' : '#F8FAFC', borderColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}")
code = code.replace("style={styles.profileDetailItem}", "style={[styles.profileDetailItem, { borderBottomColor: isDark ? '#3D3D3D' : '#E2E8F0' }]}")
code = code.replace("style={styles.profileDetailLabel}", "style={[styles.profileDetailLabel, { color: textSecondary }]}")
code = code.replace("style={styles.profileDetailValue}", "style={[styles.profileDetailValue, { color: textPrimary }]}")

# 17. Custom Alert specifics
code = code.replace("style={styles.customAlertCard}", "style={[styles.customAlertCard, { backgroundColor: bgCard }]}")
code = code.replace("style={styles.customAlertTitle}", "style={[styles.customAlertTitle, { color: textPrimary }]}")
code = code.replace("style={styles.customAlertMessage}", "style={[styles.customAlertMessage, { color: textSecondary }]}")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Theme modifications applied successfully!")
