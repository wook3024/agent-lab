class SessionStore:
    def __init__(self):
        self._sessions = {}

    def mark_active(self, user_id, session_id, epoch):
        self._sessions[user_id] = {
            "session_id": session_id,
            "epoch": epoch,
        }

    def current(self, user_id):
        return self._sessions.get(user_id)
