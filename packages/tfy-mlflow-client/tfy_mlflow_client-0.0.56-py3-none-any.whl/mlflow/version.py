import re

VERSION = "0.0.56"


def is_release_version():
    return bool(re.match(r"^\d+\.\d+\.\d+$", VERSION))
