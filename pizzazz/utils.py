from collections import Iterable
from textwrap import TextWrapper
from types import NoneType

from PIL import ImageFont


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


class Font(object):

    def __init__(self):
        super(Font, self).__init__()
        self._filename = None
        self._size = 10
        self._font = None

    def _get_size(self, text):
        if len(text) == 0:
            return 0
        size = self._font.getsize(text)
        return size

    def get_width(self, text):
        return self._get_size(text)[0]

    def get_height(self, text):
        return self._get_size(text)[1]

    @staticmethod
    def _create_font(filename, size):
        return ImageFont.truetype(filename, size)

    def _init_font(self, filename=None, size=None):
        changed = False
        if filename is None:
            filename = self._filename
        elif filename != self._filename:
            self._filename = filename
            changed = True
        if size is None:
            size = self._size
        elif size != self._size:
            self._size = size
            changed = True
        if self._font is None or changed is True:
            self._font = self._create_font(filename, size)

    @property
    def font(self):
        return self._filename

    @font.setter
    def font(self, value):
        if is_iterable(value):
            filename = value[0]
            size = value[1]
        else:
            filename = value
            size = None
        if type(filename) is not str:
            raise TypeError("Filename must be a string")
        if type(size) not in (int, NoneType):
            raise TypeError("Size must be an integer")
        self._init_font(filename, size)

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        if type(value) is not int:
            raise TypeError("Size must be an integer")
        self._init_font(size=value)


class ImageFontTextWrapper(TextWrapper):

    def __init__(self, width=70, initial_indent="", subsequent_indent="", expand_tabs=True, replace_whitespace=True,
                 fix_sentence_endings=False, break_long_words=True, drop_whitespace=True, break_on_hyphens=True, font=None):
        TextWrapper.__init__(self, width, initial_indent, subsequent_indent, expand_tabs, replace_whitespace,
                             fix_sentence_endings, break_long_words, drop_whitespace, break_on_hyphens)
        self._font = font

    def _get_width(self, text):
        return self._font.get_width(text)

    @property
    def font(self):
        return self._font

    @font.setter
    def font(self, font):
        self._font = font

    def _wrap_chunks(self, chunks):
        lines = []
        if self.width <= 0:
            raise ValueError("invalid width %r (must be > 0)" % self.width)
        if self._font is None:
            raise ValueError("imagefont not defined")

        chunks.reverse()
        while chunks:
            cur_line = []
            cur_width = 0

            if lines:
                indent = self.subsequent_indent
            else:
                indent = self.initial_indent
            width = self.width - self._get_width(indent)

            if self.drop_whitespace and chunks[-1].strip() == '' and lines:
                del chunks[-1]

            while chunks:
                w = self._get_width(chunks[-1])

                if cur_width + w <= width:
                    cur_line.append(chunks.pop())
                    cur_width += w
                else:
                    break

            if chunks and self._get_width(chunks[-1]) > width:
                self._handle_long_word(chunks, cur_line, cur_width, width)

            if self.drop_whitespace and cur_line and cur_line[-1].strip() == '':
                del cur_line[-1]

            if cur_line:
                lines.append(indent + ''.join(cur_line))

        return lines

    def wrap_font(self, text, font):
        self._font = font
        return self.wrap(text)