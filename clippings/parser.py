"""Parser for Amazon Kindle clippings file"""
import argparse
import json
import re

import dateutil.parser

from clippings.utils import BasicEqualityMixin
from clippings.utils import DatetimeJSONEncoder


DATETIME_FORMAT = '%A, %B %d, %Y %I:%M:%S %p'  # E.g. Friday, May 13, 2016 11:23:26 PM
CLIPPINGS_SEPARATOR = '=========='


class Document(BasicEqualityMixin):
    """Document (e.g. book, article) the clipping originates from.

    A document has a title, and one or multiple authors (in a string).
    """

    PATTERN = re.compile(r'^(?P<title>.+) \((?P<authors>.+?)\)$')

    def __init__(self, title, authors):
        self.title = title
        self.authors = authors

    def __str__(self):
        return '{title} ({authors})'.format(title=self.title,
                                            authors=self.authors)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def parse(cls, line):
        match = re.match(cls.PATTERN, line)
        title = match.group('title')
        authors = match.group('authors')
        return cls(title, authors)


class Location(BasicEqualityMixin):
    """Location of the clipping in the document.

    A location consists of a begin-end range.
    """

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __str__(self):
        if self.begin == self.end:
            return str(self.begin)
        else:
            return '{0}-{1}'.format(self.begin, self.end)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def parse(cls, string):
        ranges = string.split('-')
        if len(ranges) == 1:
            begin = end = ranges[0]
        else:
            begin = ranges[0]
            end = ranges[1]
        return cls(int(begin), int(end))


class Metadata(BasicEqualityMixin):
    """Metadata about the clipping:

        - The category of clipping (Note, Highlight, or Bookmark);
        - The location within the document;
        - The timestamp of the clipping;
        - The page within the document (not always present).
    """

    PATTERN = re.compile(r'^- Your (?P<category>\w+) ' +
                         r'(on|at) (page (?P<page>\d+) \| )?' +
                         r'(L|l)ocation (?P<location>\d+(-\d+)?) \| ' +
                         r'Added on (?P<timestamp>.+)$')

    HOUR_PATTERN = re.compile(r'0(\d:\d{2}:\d{2})')

    def __init__(self, category, location, timestamp, page=None):
        self.category = category
        self.location = location
        self.timestamp = timestamp
        self.page = page

    def __str__(self):
        page_string = '' if self.page is None else 'page {0} | '.format(self.page)

        # Remove leading zero's from the timestamp.
        # They are not present in the Kindle format, but can't be avoided
        # in strftime.
        timestamp_str = self.timestamp.strftime(DATETIME_FORMAT)
        timestamp_str = re.sub(self.HOUR_PATTERN, r'\1', timestamp_str)

        return '- Your {category} on {page}Location {location} | Added on {timestamp}'.format(
            category=self.category.title(),
            page=page_string,
            location=self.location,
            timestamp=timestamp_str,
        )

    def to_dict(self):
        return {
            'category': self.category,
            'location': self.location.to_dict(),
            'timestamp': self.timestamp,
            'page': self.page,
        }

    @classmethod
    def parse(cls, line):
        match = re.match(cls.PATTERN, line)
        category = match.group('category')
        location = Location.parse(match.group('location'))
        timestamp = dateutil.parser.parse(match.group('timestamp'))
        try:
            page = int(match.group('page'))
        except TypeError:
            page = None
        return cls(category, location, timestamp, page)


class Clipping(BasicEqualityMixin):
    """Kindle clipping: content associated with a particular document"""

    def __init__(self, document, metadata, content):
        self.document = document
        self.metadata = metadata
        self.content = content

    def __str__(self):
        return '\n'.join([str(self.document), str(self.metadata), str(self.content)])

    def to_dict(self):
        return {
            'document': self.document.to_dict(),
            'metadata': self.metadata.to_dict(),
            'content': self.content,
        }


def parse_clippings(clippings_file):
    """Take a file containing clippings, and return a list of objects."""

    # Last separator not followed by an entry
    entries = clippings_file.read().split(CLIPPINGS_SEPARATOR)[:-1]
    clippings = []

    for entry in entries:
        lines = entry.strip().splitlines()

        document_line = lines[0]
        document = Document.parse(document_line)

        metadata_line = lines[1]
        metadata = Metadata.parse(metadata_line)

        content = '\n'.join(lines[3:])

        clippings.append(Clipping(document, metadata, content))

    return clippings


def as_kindle(clippings):
    """Return the clippings in the original Kindle format.

    This can useful to programatically create clippings file.
    """
    string = ''
    for clipping in clippings:
        string += '\n'.join([
            str(clipping.document),
            str(clipping.metadata),
            '',
            str(clipping.content),
            CLIPPINGS_SEPARATOR,
            ''
        ])
    return string


def as_dicts(clippings):
    """Return the clippings as python dictionaries.

    The result can be converted to JSON, or manipulated directly in Python,
    for instance.
    """
    return [clipping.to_dict() for clipping in clippings]


def as_json(clippings):
    """Return the clippings as a JSON string."""
    return json.dumps(as_dicts(clippings), cls=DatetimeJSONEncoder)


def main():
    """Read the provided clippings file, parse it,
    then print it using the provided format.
    """
    parser = argparse.ArgumentParser(description='Kindle clippings parser')
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', dest='output',
                        choices=['json', 'dict', 'kindle'], default='json')
    parser.add_argument('-w', '--write-to', dest='write_to', default='-',
                        type=argparse.FileType('w'))
    args = parser.parse_args()

    clippings = parse_clippings(args.file)

    format_functions = {  # Which function to call, depending on 'output' type
        'kindle': as_kindle,
        'dict': as_dicts,
        'json': as_json,
    }
    format_function = format_functions[args.output]
    print(format_function(clippings), file=args.write_to, end='')


if __name__ == '__main__':
    main()
