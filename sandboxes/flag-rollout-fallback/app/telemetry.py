class TelemetrySink:
    def __init__(self):
        self.events = []

    def emit(self, event_name, payload):
        self.events.append((event_name, payload))


def record_exposure(flag_name, user_id, variant, telemetry):
    telemetry.emit(
        "flag_exposure",
        {
            "flag_name": flag_name,
            "user_id": user_id,
            "variant": variant,
        },
    )
