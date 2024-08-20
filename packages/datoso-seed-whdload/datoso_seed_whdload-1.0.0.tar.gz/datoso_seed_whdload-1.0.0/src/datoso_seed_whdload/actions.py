"""Actions for the whdload seed."""
from datoso_seed_whdload.dats import WhdloadDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': WhdloadDat,
        },
        {
            'action': 'DeleteOld',
            'folder': '{dat_destination}',
        },
        {
            'action': 'Copy',
            'folder': '{dat_destination}',
        },
        {
            'action': 'SaveToDatabase',
        },
    ],
}

def get_actions() -> dict:
    """Get the actions dictionary."""
    return actions
