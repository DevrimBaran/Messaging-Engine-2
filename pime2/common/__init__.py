"""
pime 2 common module

"""
import base64


def base64_encode(raw_text: str) -> str:
    """base64 utility"""
    return base64.b64encode(raw_text.encode("utf-8")).decode("ascii")


def base64_decode(raw_text: str) -> str:
    """base64 utility"""
    return base64.b64decode(raw_text.encode("ascii")).decode("ascii")
