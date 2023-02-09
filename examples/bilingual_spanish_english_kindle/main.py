from sys import argv
from pprint import pprint

from clippings.parser import parse_clippings
from .en_or_es_metadata_parser import en_or_es_metadata_parser


def print_spanish_english_parsed_clippings(clippings_fl_path: str, out_fl_path: str):
    """Parse @clippings_fl_path then print the result to @out_fl_path."""

    with open(clippings_fl_path, encoding="utf-8") as f:
        # Parse clippings using @en_or_es_metadata_parser
        clippings = parse_clippings(f, metadata_parser=en_or_es_metadata_parser)

        # Write parsed result to @out_fl_path
        with open(out_fl_path, "w", encoding="utf-8") as o:
            pprint([c.to_dict() for c in clippings], o)


# Parse a non-English clippings file:
#   python3 -m examples.bilingual_spanish_english_kindle.main \
#              ./examples/bilingual_spanish_english_kindle/resources/MyClippings.txt \
#              ./examples/bilingual_spanish_english_kindle/resources/parse_result.txt
if __name__ == "__main__":
    print_spanish_english_parsed_clippings(argv[1], argv[2])
