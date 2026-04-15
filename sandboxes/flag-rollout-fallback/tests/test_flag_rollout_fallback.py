import unittest

from app.flags import evaluate_flag
from app.telemetry import TelemetrySink


class FlagRolloutFallbackTest(unittest.TestCase):
    def test_remote_failure_fails_closed_and_deduplicates_exposure(self):
        telemetry = TelemetrySink()

        enabled = evaluate_flag(
            "new-dashboard",
            "user-1",
            {"new-dashboard": True},
            telemetry,
            should_fail=True,
        )

        self.assertFalse(enabled)
        self.assertEqual(len(telemetry.events), 1)
        event_name, payload = telemetry.events[0]
        self.assertEqual(event_name, "flag_exposure")
        self.assertEqual(payload["variant"], "disabled")


if __name__ == "__main__":
    unittest.main()
