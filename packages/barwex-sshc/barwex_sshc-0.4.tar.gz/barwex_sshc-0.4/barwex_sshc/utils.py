from os import makedirs, system
from os.path import join, dirname, exists
from .types import Sequence


def get_attr(obj, attr):
    if hasattr(obj, attr):
        return getattr(obj, attr)
    return None


def get_now_ts():
    from datetime import datetime

    return datetime.now().strftime("%Y%m%d%H%M%S")


def makedirs_ex(*dps: Sequence[str], mode: int = 511, exist_ok: bool = False):
    dp = join(*dps)
    if not exists(dp):
        makedirs(dp, mode=mode, exist_ok=exist_ok)
    return dp
