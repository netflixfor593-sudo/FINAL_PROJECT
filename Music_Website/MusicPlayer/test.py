import syncedlyrics
import re
import json

# Ask user for input
title = input("Enter Song Name: ")
artist = input("Enter Artist Name: ")

# Build query with both song + artist
query = f"{artist} {title}"
lrc = syncedlyrics.search(query)

if not lrc:
    print("No lyrics found.")
    exit()

lines = lrc.splitlines()
json_data = []

# Regex for synced lyrics: [mm:ss.xx] line_of_text
pattern = r'\[(\d+:\d+\.\d+)\](.*)'

synced = False

for line in lines:
    match = re.match(pattern, line)
    if match:
        synced = True
        timestamp, text = match.groups()
        json_entry = {
            "time": timestamp.strip(),
            "lyrics": text.strip()
        }
        json_data.append(json_entry)

if not synced:
    # Handle plain lyrics (no timestamps)
    for line in lines:
        if line.strip():
            json_entry = {
                "time": None,
                "lyrics": line.strip()
            }
            json_data.append(json_entry)

# Convert to JSON
json_string = json.dumps(json_data, indent=4, ensure_ascii=False)

print(json_string)

