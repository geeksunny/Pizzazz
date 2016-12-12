from collections import Iterable


def is_iterable(obj):
    return isinstance(obj, Iterable)

def not_implemented(clazz, method_name):
    return "Class {} does not implement {}".format(clazz.__class__.__name__, method_name)


class Singleton(type):

    _instances = {}

    def __call__(cls, *more):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*more)
        return cls._instances[cls]
