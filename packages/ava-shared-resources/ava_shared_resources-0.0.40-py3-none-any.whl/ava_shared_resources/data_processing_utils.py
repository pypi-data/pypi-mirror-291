"""Text processing functions."""

import re

import ftfy
from bs4 import BeautifulSoup

space_pattern = re.compile(r"\s\s+")

typography_mapping = {
    "Ꜳ": "AA",
    "ꜳ": "aa",
    "Æ": "AE",
    "æ": "ae",
    "Ꜵ": "AO",
    "ꜵ": "ao",
    "Ꜷ": "AU",
    "ꜷ": "au",
    "Ꜹ": "AV",
    "ꜹ": "av",
    "Ꜽ": "AY",
    "ꜽ": "ay",
    "ﬀ": "ff",
    "ﬃ": "ffi",
    "ﬄ": "ffl",
    "ﬁ": "fi",
    "ﬂ": "fl",
    "Œ": "OE",
    "œ": "oe",
    "Ꝏ": "OO",
    "ꝏ": "oo",
    "ﬆ": "st",
    "ﬅ": "ft",
    "ᵫ": "ue",
    "Ꝡ": "VY",
    "ꝡ": "vy",
    "\xa0": " ",  # non-breaking space
    "\u200b": " ",  # zero-width space
}


def rm_extra_space(text: str) -> str:
    """Remove extra spaces from the text.

    It removes the multiple spaces and spaces at the beginning and end of the text.
    :param text: text to normalize.
    :return: normalized text.
    """
    return space_pattern.sub(" ", text.strip())


def typography_to_plain(text: str) -> str:
    """Replace certain typographical entities (ligatures, zero-width spaces, etc) with their plain text alternatives.

    :param text: text.
    :return: plain text.
    """
    for initial, replacement in typography_mapping.items():
        text = text.replace(initial, replacement)
    return text


def html_to_plain(html_text: str) -> str:
    """Convert HTML text into plain text.

    :param html_text: HTML text.
    :return: plain text.
    """
    text = ftfy.fixes.unescape_html(html_text)
    text = BeautifulSoup(text, "lxml").get_text(separator=" ")
    text = ftfy.fix_text(text)
    text = typography_to_plain(text)
    text = rm_extra_space(text)
    return text
