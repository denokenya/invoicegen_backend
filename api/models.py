from hashlib import blake2s
from django.utils import timezone


def today():
    return timezone.localtime(timezone.now())


def generalCode(length):
    code = blake2s(digest_size=length // 2)
    code.update(bytes(f"{today()}", "utf-8"))
    return f"MT{code.hexdigest()}".upper()
