import re
import json

def normalize_speaker(name):
    name = name.strip().lower()

    # 🔥 normalize YOUR name
    if "bhoomi" in name:
        return "Bhoomi"

    # 🔥 map your people
    elif "priyanshi" in name:
        return "Priyanshi"
    elif "mosham" in name:
        return "Mosam"
    elif "anuraag" in name:
        return "Anuraag"
    elif "bhumika" in name:
        return "Bhumika"

    return name.title()  # fallback


def parse_chat(file_path):
    pattern = r'^(\d{1,2}/\d{1,2}/\d{2,4}),\s(.+?)\s-\s([^:]+):\s(.*)'
    messages = []

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(pattern, line.strip())

            if match:
                _, _, speaker, message = match.groups()

                speaker = normalize_speaker(speaker)
                message = message.strip()

                # 🚫 skip useless data
                if not message:
                    continue

                if "<media omitted>" in message.lower():
                    continue

                if message in ["ok", "okk", "k", "hmm"]:
                    continue

                messages.append({
                    "speaker": speaker,
                    "message": message
                })

    return messages


# 🔁 run parser
data = parse_chat("data/raw/chat.txt")

# save
with open("data/processed/messages.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("Clean messages saved:", len(data))