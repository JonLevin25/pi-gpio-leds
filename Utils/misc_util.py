
def is_iter(obj):
    if obj is None:
        return False
    return getattr(obj, "__iter__", None) is not None
