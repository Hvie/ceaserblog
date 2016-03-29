# config.py

import config_default

try:
    import config_override
    configs = merge(configs, config_override.configs)
except Import Error:
    pass
