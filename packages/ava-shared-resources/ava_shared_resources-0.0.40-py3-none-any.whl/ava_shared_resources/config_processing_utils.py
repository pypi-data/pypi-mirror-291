"""functions for configuration processing."""


def merge_configs(conf: dict, conf_for_merge: dict):
    """Recursively merge two dictionaries.

    Merges the configuration dictionaries in recursive way
    :param conf: config for updating.
    :param conf_for_merge: config that contains values for updating and replacing the config's values.
    :return: merged config.
    """
    for key, value in conf_for_merge.items():
        if key in conf and isinstance(conf[key], dict) and isinstance(value, dict):
            conf[key] = merge_configs(conf[key], value)
        else:
            conf[key] = value
    return conf
