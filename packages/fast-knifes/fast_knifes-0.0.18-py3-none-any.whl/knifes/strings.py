def blur_phone(phone):
    """blur phone number"""
    if not phone or len(phone) < 11:
        return phone
    return phone[:3] + "****" + phone[7:]


def abbreviate(text, max_len=2, marker="..."):
    """slice text to max_len and add marker if text is too long"""
    return text[0:max_len] + marker if len(text) > max_len else text


def ensure_str(x: bytes | str):
    """convert bytes to str"""
    return x.decode() if isinstance(x, bytes) else x


def ensure_bytes(x: bytes | str):
    """convert str to bytes"""
    return x.encode() if isinstance(x, str) else x


class String(str):
    """str object to which attributes can be added"""
