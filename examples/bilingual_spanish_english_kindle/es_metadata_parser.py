from clippings.parser import Location
from .utils import (Category, MetadataParsers, bind_parsers,
                    create_metadata_parser, date_parser, int_parser, pattern_parser)


def es_category_parser(category_str) -> Category:
    if category_str == 'subrayado':
        return Category.HIGHLIGHT
    elif category_str == 'marcador':
        return Category.BOOKMARK
    elif category_str == 'nota':
        return Category.NOTE


es_metadata_parsers: MetadataParsers = {
    "location": bind_parsers(
        Location.parse,
        pattern_parser(r'posición ([\d-])+')),
    "page": bind_parsers(int_parser, pattern_parser(r'página (\d)+')),
    "timestamp": bind_parsers(
        date_parser(
            'el %A, %d de %B de %Y %H:%M:%S',
            locale='es_ES.UTF-8'),
        pattern_parser(r'Añadido (.+)', True)),
    "category": bind_parsers(
        es_category_parser,
        pattern_parser(r'(?:El|La) (\w+)', True))
}

es_metadata_parser = create_metadata_parser(**es_metadata_parsers)
