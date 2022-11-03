from clippings.parser import Location
from .utils import (Category, MetadataParsers, ParseError, bind_parsers,
                    create_metadata_parser, date_parser, pattern_parser)


def en_category_parser(category_str) -> Category:
    for cat in Category:
        if category_str.casefold() == cat.name.casefold():
            return cat

    raise ParseError(category_str, Category)


en_metadata_parsers: MetadataParsers = {
    "location": bind_parsers(
        Location.parse,
        pattern_parser(r'location ([\d-])+')),
    "page": bind_parsers(int_parser, pattern_parser(r'page ([\d-])+')),
    "timestamp": bind_parsers(
        date_parser('%A, %d %B %Y %H:%M:%S'),
        pattern_parser(r'Added on (.+)', True)),
    "category": bind_parsers(en_category_parser, pattern_parser(r'Your (\w+)', True))
}

en_metadata_parser = create_metadata_parser(**en_metadata_parsers)
