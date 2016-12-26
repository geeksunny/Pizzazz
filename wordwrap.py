#!/usr/bin/python
from PIL import ImageFont
from collections import namedtuple
import re

# work in progress code for wordwrap algorithm. To be merged into render.py

font_size = 12
screen_width = 128
test_str = "The quick brown fox jumps over the lazy dog."
font = ImageFont.truetype("/Users/Sunny/Documents/pizzazz/fonts/Super-Mario-World.ttf", font_size)

Range = namedtuple("Range", "start end")


def _find_punctuation_break(text):
    regex = re.compile(r"\S*([\.\?\]\)\}\|\;]+)\s*$")
    match = regex.search(text)
    if match and len(match.groups()):
        return Range(match.start(1), match.end(1))
    else:
        return None


def _find_last_whitespace(text):
    regex = re.compile(r"([\n\r\s]+)\S+$")
    match = regex.search(text)
    if match and len(match.groups()):
        return Range(match.start(1), match.end(1))
    else:
        return None


def _get_substring(text):
    p_break = _find_punctuation_break(text)
    pass
    whitespace = _find_last_whitespace(text)
    pass
    pass


def _remove_line(text, length):
    try:
        return text[length:]
    except IndexError:
        return ""


def difference(a, b):
    high, low = (a, b) if a > b else (b, a)
    return high - low


def midpoint(a, b):
    if a == b:
        return a
    high, low = (a, b) if a > b else (b, a)
    mid = int((high - low) / 2) + low
    return mid


def _text_fits(text, width):
    size = font.getsize(text)
    return size[0] <= width


def _word_wrap(text, width):
    lines = []
    processing = True
    while processing:
        text = text.strip()
        if len(text) == 0:
            break
        pos = len(text)
        fit = failure = None
        line_complete = False
        while not line_complete:
            substr = text[:pos]
            whitespace = _find_last_whitespace(substr)
            if whitespace:
                pos = whitespace.start
                substr = text[:pos]
            print "pos: {} | substr: {}".format(pos, substr)
            if _text_fits(substr, width):
                print " -fits"
                fit = pos
                if failure is None or failure == fit + 1:
                    # or fit == len(text)
                    lines.append(substr)
                    text = _remove_line(text, pos)
                    break
            else:
                print " -does not fit"
                failure = pos
                if fit is None:
                    fit = 0
            pos = midpoint(fit, failure)
    return lines


if __name__ == "__main__":
    print "starting w: {}".format(test_str)
    print
    wrapped_lines = _word_wrap(test_str, screen_width)
    print
    print wrapped_lines
    print
    print "Done"
