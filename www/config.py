# config.py

import config_default

class cdict(dict):
    '''
    Simple dict but support access as x.y style
    '''
    def __init__(self, names=(), values=(), **kw):
        super(cdict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r'"Dict" object has no attribute "%s" ' & key)

    def __setattr__(self, key, value):
        self[key] = value


def merge(raw, override):
    # 很清楚的递归调用就能解决这个事情
    r = {}
    for k, v in raw.items():
        if k in override:
            if isinstance(v, dict):
                r[k] = merge(v, override[k])
            else:
                r[k] = override[k]
        else:
            r[k] = v
    return r

def tocdict(d):
    # 递归地将dict与dict中的dict均转为cdict
    C = cdict()
    for k, v in d.items():
        C[k] = tocdict(v) if isinstance(v, dict) else v
    return C

configs = config_default.configs

try:
    import config_override
    configs = merge(configs, config_override.configs)
except ImportError:
    pass

configs = tocdict(configs)
