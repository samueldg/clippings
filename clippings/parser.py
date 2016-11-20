"""Parser for Amazon Kindle clippings file"""

import argparse
import json
import re

import dateutil.parser

from clippings.utils import DatetimeJSONEncoder


DATETIME_FORMAT = '%A, %B %d, %Y %I:%M:%S %p'  # E.g. Friday, May 13, 2016 11:23:26 PM
CLIPPINGS_SEPARATOR = '=========='


class Document:
    """Document (e.g. book, article) the clipping originates from.

    A document has a title, and a list of authors.
    """

    PATTERN = re.compile(r'^(?P<title>.+)\((?P<authors>.+?)\)$')
    AUTHORS_SEPARATOR = ';'

    def __init__(self, title, authors):
        self.title = title
        self.authors = authors

    def __repr__(self):
        authors_string = self.AUTHORS_SEPARATOR.join(self.authors)
        return '{title} ({authors})'.format(title=self.title,
                                            authors=authors_string)

    def to_dict(self):
        return self.__dict__

    @classmethod
    def parse(cls, line):
        match = re.match(cls.PATTERN, line)
        title = match.group('title')
        authors_string = match.group('authors')
        authors = authors_string.split(cls.AUTHORS_SEPARATOR)
        return cls(title, authors)


class Location:
    """Location of the clipping in the document.

    A location consists of a begin-end range.
    """

    def __init__(self, begin, end):
        self.begin = begin
        self.end = end

    def __repr__(self):
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


class Metadata:
    """Metadata about the clipping:

        - The category of clipping (Note, Highlight, or Bookmark);
        - The location within the document;
        - The timestamp of the clipping;
        - The page within the document (not always present).
    """

    PATTERN = re.compile(r'^- Your (?P<category>\w+) ' +
                         r'on (page (?P<page>\d+) \| )?' +
                         r'Location (?P<location>\d+(-\d+)?) \| ' +
                         r'Added on (?P<timestamp>.+)$')

    def __init__(self, category, location, timestamp, page=None):
        self.category = category
        self.location = location
        self.timestamp = timestamp
        self.page = page

    def __repr__(self):
        page_string = '' if self.page is None else 'page {0} | '.format(self.page)

        return '- Your {category} on {page}Location {location} | Added on {timestamp}'.format(
            category=self.category.title(),
            page=page_string,
            location=self.location,
            timestamp=self.timestamp.strftime(DATETIME_FORMAT),
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
            page = match.group('page')
        except TypeError:
            page = None
        return cls(category, location, timestamp, page)


class Clipping:
    """Kindle clipping: content associated with a particular document"""

    def __init__(self, document, metadata, content):
        self.document = document
        self.metadata = metadata
        self.content = content

    def __repr__(self):
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

        content = '\n'.join(lines[2:])

        clippings.append(Clipping(document, metadata, content))

    return clippings


def main():
    """Read the provided clippings file, parse it,
    then print it using the provided format.
    """
    parser = argparse.ArgumentParser(description='Kindle clippings parser')
    parser.add_argument('file', type=argparse.FileType('r'))
    parser.add_argument('-o', '--output', dest='output',
                        choices=['json', 'dict', 'kindle'], default='json')
    args = parser.parse_args()

    clippings = parse_clippings(args.file)

    if args.output == 'kindle':
        for clipping in clippings:
            print(clipping.document)
            print(clipping.metadata)
            print(clipping.content)
            print(CLIPPINGS_SEPARATOR)

    if args.output == 'dict':
        for clipping in clippings:
            print(clipping.to_dict())

    elif args.output == 'json':
        for clipping in clippings:
            print(json.dumps(clipping.to_dict(), cls=DatetimeJSONEncoder))

if __name__ == '__main__':
    main()
