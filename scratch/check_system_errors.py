import os

app_data_dir = r"C:\Users\Sharli\.gemini\antigravity"
conv_id = "0c674d5e-09e5-429e-882a-1f55c9fdc861"
transcript_path = os.path.join(
    app_data_dir, "brain", conv_id, ".system_generated", "logs", "transcript.jsonl"
)

if not os.path.exists(transcript_path):
    print("Transcript not found at", transcript_path)
    sys.exit(0)

print("Searching transcript.jsonl for error traces...")
found = False
with open(transcript_path, "r", encoding="utf-8") as f:
    for line in f:
        if "actualizar foto" in line or "foto de perfil" in line or "ImagePicker" in line:
            print(line[:400])
            found = True

if not found:
    print("No profile photo error logs found in transcript.")
