from collections import Iterable


def is_iterable(obj):
    return isinstance(obj, Iterable)


def not_implemented(clazz, method_name):
    return "Class {} does not implement {}".format(clazz.__class__.__name__, method_name)


def midpoint(a, b):
    if a == b:
        return a
    high, low = (a, b) if a > b else (b, a)
    mid = int((high - low) / 2) + low
    return mid


class Singleton(type):

    _instances = {}

    def __call__(cls, *more):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*more)
        return cls._instances[cls]


class TextAlignment(object):

    LEFT = "left"
    RIGHT = "right"
    CENTER = "center"
    JUSTIFY = "justify"

    @staticmethod
    def is_valid(value):
        return value in (TextAlignment.LEFT, TextAlignment.RIGHT, TextAlignment.CENTER, TextAlignment.JUSTIFY)