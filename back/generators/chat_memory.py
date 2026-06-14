# ---------------------------------------------------
# SIMPLE IN-MEMORY CHAT STORAGE
# ---------------------------------------------------

conversation_store = {}

# ---------------------------------------------------
# GET CHAT HISTORY
# ---------------------------------------------------

def get_history(user_id):

    return conversation_store.get(user_id, [])

# ---------------------------------------------------
# SAVE MESSAGE
# ---------------------------------------------------

def save_message(user_id, role, content):

    if user_id not in conversation_store:

        conversation_store[user_id] = []

    conversation_store[user_id].append(
        {
            "role": role,
            "content": content
        }
    )

    # Keep only recent messages

    conversation_store[user_id] = (
        conversation_store[user_id][-20:]
    )

# ---------------------------------------------------
# CLEAR CHAT
# ---------------------------------------------------

def clear_history(user_id):

    if user_id in conversation_store:

        conversation_store[user_id] = []