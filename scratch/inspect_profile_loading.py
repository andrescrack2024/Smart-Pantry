file_path = r"c:\Users\Sharli\Documents\Nueva carpeta (2)\proyecto smart-pantry\smart-pantry\src\screens\HomeScreen.js"

with open(file_path, "r", encoding="utf-8") as f:
    code = f.read()

import re

# Find all occurrences of 'users' in Firestore calls
firestore_calls = re.findall(
    r"[a-zA-Z0-9_]+\(doc\(db,\s*'users',.*?\)", code, re.DOTALL
)
print("Firestore calls on 'users' collection:")
for call in set(firestore_calls):
    print("  ", call.strip())
