DEFAULT_CONFIG = {
    'tolerance': 1e-8,
    'structure_check': False,
    'modules': "",
    'check_for': False,
    'check_while': False,
    'check_loop': False,
    'display_answer': True,
    'max_wrong_times': 3,
    'ai_in_use': True
}

CONFIG = {}


def change_default_config(config: dict):
    global DEFAULT_CONFIG
    config_keys = config.keys()
    intersection = config_keys & DEFAULT_CONFIG.keys()
    diff = config_keys - intersection
    if len(diff) != 0:
        print(f"The config name: {diff} not defined")
    for key, value in DEFAULT_CONFIG.items():
        if key in config_keys:
            DEFAULT_CONFIG[key] = config[key]


def change_config(config: dict):
    global DEFAULT_CONFIG, CONFIG
    if config == {}:
        return

    config_keys = config.keys()
    intersection = config_keys & DEFAULT_CONFIG.keys()
    diff = config_keys - intersection
    if len(diff) != 0:
        print(f"The config name: {diff} not defined")
    for key, value in DEFAULT_CONFIG.items():
        if key in config_keys:
            CONFIG[key] = config[key]
        else:
            CONFIG[key] = value


def get_default_config():
    return DEFAULT_CONFIG


def get_config():
    return CONFIG if CONFIG != {} else DEFAULT_CONFIG


if __name__ == '__main__':
    change_default_config({'tolerance': 1e-7})
    print(DEFAULT_CONFIG)
