import json

# Load messages
with open("data/processed/messages.json", "r", encoding="utf-8") as f:
    messages = json.load(f)

TARGET = "Bhoomi"

pairs = []

bad_replies = ["ok", "okk", "k", "hmm", "ni", "😂", "😂😂"]

for i in range(1, len(messages)):
    prev = messages[i - 1]
    curr = messages[i]

    # Only when YOU reply
    if curr["speaker"] == TARGET and prev["speaker"] != TARGET:

        context = prev["message"].strip()
        reply = curr["message"].strip().lower()

        # 🚫 skip bad data
        if not context or not reply:
            continue

        if "<media omitted>" in context.lower():
            continue

        if len(reply.split()) < 2:
            continue

        if reply in bad_replies:
            continue

        # 👇 YOUR CUSTOM PERSON MAPPING
        other = prev["speaker"].lower()

        if "mosam" in other:
            person = "best_friend"
        elif "priyanshi" in other:
            person = "best_friend"
        elif "anuraag" in other:
            person = "friend"
        elif "bhumika" in other:
            person = "friend"
        else:
            person = "other"

        pairs.append({
            "context": f"{person}: {context}",
            "reply": curr["message"]
        })

# Save pairs
with open("data/processed/pairs.json", "w", encoding="utf-8") as f:
    json.dump(pairs, f, indent=2, ensure_ascii=False)

print("Clean pairs created:", len(pairs))