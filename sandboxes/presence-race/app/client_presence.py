def merge_presence(online_state, user_id, session_id, state):
    if state == "connected":
        online_state[user_id] = session_id
    elif state == "disconnected":
        online_state.pop(user_id, None)
