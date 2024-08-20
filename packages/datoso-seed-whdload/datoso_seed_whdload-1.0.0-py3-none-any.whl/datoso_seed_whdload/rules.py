"""Rules for the Whdload seed."""
from datoso_seed_whdload.dats import WhdloadDat

rules = [
    {
        'name': 'Whdload Dat',
        '_class': WhdloadDat,
        'seed': 'Whdload',
        'priority': 0,
        'rules': [
            {
                'key': 'url',
                'operator': 'contains',
                'value': 'www._whdload.org',
            },
            {
                'key': 'homepage',
                'operator': 'eq',
                'value': '_whdload',
            },
        ],
    },
]


def get_rules() -> list:
    """Get the rules."""
    return rules
