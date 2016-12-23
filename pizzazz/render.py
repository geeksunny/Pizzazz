import re
from collections import namedtuple
from types import NoneType

from PIL import ImageFont

from utils import TextAlignment, not_implemented, is_iterable, midpoint

# TODO: Screens should use the renderers as the method for drawing window contents

Rect = namedtuple("Rect", "left top right bottom",)
Point = namedtuple("Point", "x y")
Range = namedtuple("Range", "start end")


class AbstractRenderer(object):

    def __init__(self):
        super(AbstractRenderer, self).__init__()

    def render(self):
        raise NotImplementedError(not_implemented(self, "render()"))


class TextRenderer(AbstractRenderer):

    def __init__(self):
        super(TextRenderer, self).__init__()
        self._font = None
        self._font_filename = None
        self._font_size = 10
        self._alignment = TextAlignment.LEFT
        self._text = ""

    @staticmethod
    def _create_font(filename, size):
        return ImageFont.truetype(filename, size)

    def _init_font(self, filename=None, size=None):
        changed = False
        if filename is None:
            filename = self._font_filename
        elif filename != self._font_filename:
            self._font_filename = filename
            changed = True
        if size is None:
            size = self._font_size
        elif size != self._font_size:
            self._font_size = size
            changed = True
        if self._font is None or changed is True:
            self._font = self._create_font(filename, size)

    @property
    def font(self):
        return self._font_filename

    @font.setter
    def font(self, value):
        if is_iterable(value):
            filename = value[0]
            size = value[1]
        else:
            filename = value
            size = None
        if type(filename) is not str:
            raise TypeError("Filename must be a string.")
        if type(size) not in (int, NoneType):
            raise TypeError("Size must be an integer.")
        self._init_font(filename, size)

    @property
    def size(self):
        return self._font_size

    @size.setter
    def size(self, value):
        if type(value) is not int:
            raise TypeError("Size must be an integer.")
        self._init_font(size=value)

    @property
    def alignment(self):
        return self._alignment

    @alignment.setter
    def alignment(self, value):
        if TextAlignment.is_valid(value):
            self._alignment = value
        else:
            raise TypeError("Invalid alignment value provided.")

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    def _text_fits(self, text, width):
        size = self._font.getsize(text)
        return size[0] <= width

    def _split_lines(self, text):
        regex = re.compile(r"[\n\r]")
        return regex.split(text)

    def _find_word_breaks(self, text):
        breaks = []
        regex = re.compile(r"\s+")
        matches = regex.finditer(text)
        for match in matches:
            break_ = Range(match.start(), match.end())
            breaks.append(break_)
        return breaks

    def _find_last_whitespace(self, text):
    # TODO: Is this method necessary?
        regex = re.compile(r"([\n\r\s]+)\S+$")
        match = regex.search(text)
        if match and len(match.groups()):
            return Range(match.start(1), match.end(1))
        else:
            return None

    # TODO: Merge code from wordwrap.py in with these methods
    # def _word_wrap(self, text, width):
    #     # TODO: Try some math-based algorithm for detecting wrap-breaks.
    #     # if line does not fit, check if half of the line fits.
    #     # if half-line does not fit, check half-way between half-line and beginning.
    #     # if half-line does fit, check halfway between half-line and end.
    #     # Bounce back and forth before finding the max-length of text that fits. \
    #     lines = []
    #     processing = True
    #     while processing:
    #         pos = len(text)
    #         fit = failure = None
    #         line_complete = False
    #         while not line_complete:
    #             substr = text[:pos]
    #             if self._text_fits(substr, width):
    #                 # TODO: Add in code that considers closest whitespace position
    #                 fit = pos
    #                 if failure is None: # if pos == len:
    #                     lines.append(substr)
    #                     processing = False
    #                     break
    #                 high, low = (fit, failure) if fit >= failure else failure, fit
    #                 pos = int()
    #                 if pos > len(text):
    #                     pass
    #                 try:
    #                     excess = text[pos]
    #                     lines.extend(self._word_wrap(excess, width))
    #                 except IndexError:
    #                     # Do nothing here because excess went out of bounds so nothing is left.
    #                     pass
    #                 processing = True
    #             else:
    #                 failure = pos
    #                 #todo adjust position
    #             # new position
    #             pos = midpoint(fit, failure)
    #
    #     return lines
    #
    # def _get_wrap_lines(self, text, width):
    #     lines = self._split_lines(text)
    #     wrapped_lines = []
    #     for line in lines:
    #         word_breaks = self._find_word_breaks(line)
    #         word_breaks.reverse()
    #         if self._text_fits(line, width):
    #             wrapped_lines.append(line)
    #             break
    #         for word_break in word_breaks:
    #             substr = line[:word_break.start]
    #             if self._text_fits(substr, width):
    #                 wrapped_lines.append(substr)
    #                 excess = line[word_break.end:]
    #                 wrapped_lines.append(self._get_wrap_lines(excess, width))
    #                 # todo: push the excess to be the next item processed...
    #     return lines


class ListRenderer(AbstractRenderer):
    pass