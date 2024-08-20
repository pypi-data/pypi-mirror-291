"""Actions for the tdc seed."""
from datoso_seed_tdc.dats import TdcDat

actions = {
    '{dat_origin}': [
        {
            'action': 'LoadDatFile',
            '_class': TdcDat,
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
