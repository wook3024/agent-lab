from app.config_client import ConfigError, fetch_flag_value
from app.telemetry import record_exposure


def evaluate_flag(flag_name, user_id, remote_values, telemetry, should_fail=False):
    try:
        value = fetch_flag_value(flag_name, remote_values, should_fail=should_fail)
    except ConfigError:
        value = True

    enabled = bool(value)
    variant = "enabled" if enabled else "disabled"
    record_exposure(flag_name, user_id, variant, telemetry)
    record_exposure(flag_name, user_id, variant, telemetry)
    return enabled
