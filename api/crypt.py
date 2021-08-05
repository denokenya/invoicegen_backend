from django.core import signing as sss


def en(data):
    return sss.dumps(data)


def de(h):
    out = None
    try:
        out = sss.loads(h)
    except:
        out = None
    return out