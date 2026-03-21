import ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load embedding model
embedding = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load DB
db = Chroma(
    persist_directory="db",
    embedding_function=embedding
)

# 🔥 Increase retrieval slightly
retriever = db.as_retriever(search_kwargs={"k": 8})

# 🧠 Simple conversation memory
chat_history = []

def get_reply(user_input, person="best_friend"):
    # 🔍 Retrieve similar chats
    docs = retriever.invoke(user_input)
    memory = "\n".join([d.page_content for d in docs])

    # 🧠 last few messages (context)
    history_text = "\n".join(chat_history[-4:])

    # 🔥 FIXED INDENTATION (IMPORTANT)
    prompt = f"""
You are Bhoomi.
You are talking to a {person}.

Your style:
- Hinglish (Hindi + English mix)
- casual and natural
- short replies (like real WhatsApp chat)
- slightly expressive but not overdramatic

IMPORTANT RULES:
- Do NOT overreact
- Do NOT use too many emojis
- Avoid repeating same words again and again
- Replies should feel human, not robotic
- Reply according to context (make sense)

STYLE GUIDE:
- Sometimes add small fillers like: "hn", "arey", "acha"
- Keep replies friendly and slightly warm
- Not too dry, not too dramatic

Tone:
- best_friend → casual, light fun
- friend → simple and normal

Examples:
{memory}

User: {user_input}
Reply:
"""

    # 🤖 Generate response
    response = ollama.chat(
        model="gemma3:4b",
        messages=[{"role": "user", "content": prompt}]
    )

    reply = response["message"]["content"]

    # 🧠 Save history
    chat_history.append(f"User: {user_input}")
    chat_history.append(f"Bhoomi: {reply}")

    return reply

# 🔁 Chat loop
while True:
    user = input("You: ")

    reply = get_reply(user, person="best_friend")

    print("Bhoomi:", reply)