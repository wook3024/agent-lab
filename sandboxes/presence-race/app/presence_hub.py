from app.client_presence import merge_presence


def apply_presence_event(user_id, event, session_store, online_state):
    if event["state"] == "connected":
        session_store.mark_active(user_id, event["session_id"], event["epoch"])

    merge_presence(online_state, user_id, event["session_id"], event["state"])
    return online_state
