from .en_metadata_parser import en_metadata_parser
from .es_metadata_parser import es_metadata_parser
import re


def en_or_es_metadata_parser(metadata_line: str):
    """Parse @metadata_line in Spanish or English"""
    if re.search("Your", metadata_line):
        return en_metadata_parser(metadata_line)
    else:
        return es_metadata_parser(metadata_line)
