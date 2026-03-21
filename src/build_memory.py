import json

# Load pairs
with open("data/processed/pairs.json", "r", encoding="utf-8") as f:
    pairs = json.load(f)

memory = []

bad_words = ["ok", "okk", "k", "hmm", "ni"]

for p in pairs:
    context = p["context"].strip().lower()
    reply = p["reply"].strip().lower()

    # 🚫 skip empty
    if not context or not reply:
        continue

    # 🚫 skip very short replies
    if len(reply.split()) < 2:
        continue

    # 🚫 skip useless replies
    if reply in bad_words:
        continue

    # 🚫 skip emoji-only replies
    if all(char in "😂😭🥹🤣😅" for char in reply):
        continue

    # 🔥 NEW: skip bad context
    context_text = context.split(":", 1)[-1].strip()

    if len(context_text.split()) < 2:
        continue

    if all(char in "😂😭🥹🤣😅" for char in context_text):
        continue

    # ✅ clean memory entry
    memory.append({
        "page_content": f"{p['context']}\nBhoomi: {p['reply']}",
        "metadata": {
            "reply": p["reply"]
        }
    })

# Save memory
with open("data/processed/memory.json", "w", encoding="utf-8") as f:
    json.dump(memory, f, indent=2, ensure_ascii=False)

print("Clean memory created:", len(memory))