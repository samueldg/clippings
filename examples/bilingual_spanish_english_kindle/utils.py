import contextlib
import locale as locale_module
import re
from datetime import datetime
from enum import Enum, auto
from typing import Optional, TypedDict, Callable

from clippings.parser import Metadata, Location


class ParseError(Exception):
    def __init__(self, string, parsing_as):
        super().__init__(f"Failed to parse {string} as {parsing_as}")


class Category(Enum):
    """
    Category allows users to normalise the result of metadata line parsing
    across languages.

    For example, the metadata lines

    "- La subrayado en la página 4 | posición 60-60 | Añadido el miércoles, 6 de julio de 2022 06:54:57"
    "- Your Highlight on page 4 | location 60-60 | Added on Wednesday, 6 July 2022 06:54:57"

    represent the same highlight but in different languages, so we may wish to
    parse them both as { "category": Category.HIGHLIGHT, ... }.
    """  # noqa: E501
    NOTE = auto()
    HIGHLIGHT = auto()
    BOOKMARK = auto()


@contextlib.contextmanager
def setlocale(*args, **kw):
    """ With thanks: https://stackoverflow.com/a/18594128
    """
    saved = locale_module.setlocale(locale_module.LC_ALL)
    yield locale_module.setlocale(*args, **kw)
    locale_module.setlocale(locale_module.LC_ALL, saved)


def pattern_parser(pattern, raise_parse_failure=False):
    def parser(s: str) -> Optional[str]:
        match = re.search(pattern, s)
        if match:
            return match.group(1)
        elif raise_parse_failure:
            raise ParseError(s, str)

    return parser


def date_parser(date_format, locale=None):
    def parser(s: str):
        if locale:
            with setlocale(locale_module.LC_TIME, locale):
                return datetime.strptime(s, date_format)
        else:
            return datetime.strptime(s, date_format)

    return parser


def int_parser(s: str):
    try:
        return int(s)
    except TypeError:
        return None


def bind_parsers(parser1, parser2):
    def parser(s: str):
        res = parser2(s)
        if res:
            return parser1(res)

    return parser


class MetadataParsers(TypedDict):
    category: Callable[[str], str]
    page: Callable[[str], Optional[int]]
    location: Callable[[str], Location]
    timestamp: Callable[[str], datetime]


def create_metadata_parser(**parsers):
    def parser(metadata_line: str):
        return Metadata(
            category=parsers['category'](metadata_line),
            location=parsers['location'](metadata_line),
            timestamp=parsers['timestamp'](metadata_line),
            page=parsers['page'](metadata_line))

    return parser
