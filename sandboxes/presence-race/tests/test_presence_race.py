import unittest

from app.presence_hub import apply_presence_event
from app.session_store import SessionStore


class PresenceRaceTest(unittest.TestCase):
    def test_stale_event_does_not_replace_newer_session(self):
        store = SessionStore()
        online_state = {}

        apply_presence_event(
            "user-1",
            {"session_id": "new", "epoch": 2, "state": "connected"},
            store,
            online_state,
        )
        apply_presence_event(
            "user-1",
            {"session_id": "old", "epoch": 1, "state": "connected"},
            store,
            online_state,
        )

        self.assertEqual(store.current("user-1")["session_id"], "new")
        self.assertEqual(online_state["user-1"], "new")


if __name__ == "__main__":
    unittest.main()
