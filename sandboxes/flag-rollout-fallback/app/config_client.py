class ConfigError(Exception):
    pass


def fetch_flag_value(flag_name, remote_values, should_fail=False):
    if should_fail:
        raise ConfigError(f"failed to fetch {flag_name}")
    return remote_values.get(flag_name)
