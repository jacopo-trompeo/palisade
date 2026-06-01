from palisade.config import DEV_MODE

if DEV_MODE:
    from palisade.db.database import (
        get_setting as get_setting,
    )
    from palisade.db.database import (
        set_setting as set_setting,
    )
else:
    pass
