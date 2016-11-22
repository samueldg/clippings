import datetime
import unittest

from clippings.parser import Document
from clippings.parser import Location
from clippings.parser import Metadata


class DocumentTest(unittest.TestCase):

    def test_create_document(self):
        title = 'Haunted'
        authors = ['Chuck Palahniuk']
        document = Document(title, authors)

        self.assertEqual(title, document.title)
        self.assertEqual(authors, document.authors)

    def test_parse_document_with_single_author(self):
        document_line = '1984 (George Orwell)'
        document = Document.parse(document_line)

        expected_authors = ['George Orwell']
        self.assertEqual(expected_authors, document.authors)

        expected_title = '1984'
        self.assertEqual(expected_title, document.title)

    def test_parse_document_with_multiple_authors(self):
        document_line = 'Java Concurrency in Practice (Joshua Bloch;Brian Goetz)'
        document = Document.parse(document_line)

        expected_authors = [
            'Joshua Bloch',
            'Brian Goetz',
        ]
        self.assertEqual(expected_authors, document.authors)

        expected_title = 'Java Concurrency in Practice'
        self.assertEqual(expected_title, document.title)

    def test_document_to_string(self):
        title = 'Also sprach Zarathustra'
        authors = ['Friedrich Nietzsche']
        document = Document(title, authors)

        expected_string = 'Also sprach Zarathustra (Friedrich Nietzsche)'
        self.assertEqual(expected_string, str(document))

    def test_document_to_dict(self):
        title = 'À la recherche du temps perdu'
        authors = ['Marcel Proust']
        document = Document(title, authors)

        expected_dict = {
            'title': title,
            'authors': authors
        }
        self.assertEqual(expected_dict, document.to_dict())


class LocationTest(unittest.TestCase):

    BEGIN = 666
    END = 1337
    SINGLE_LOCATION_STRING = '666'
    RANGE_LOCATION_STRING = '666-1337'

    def test_create_location(self):
        location = Location(self.BEGIN, self.END)
        self.assertEqual(self.BEGIN, location.begin)
        self.assertEqual(self.END, location.end)

    def test_parse_range_location(self):
        location_string = self.RANGE_LOCATION_STRING
        location = Location.parse(location_string)
        self.assertTrue(isinstance(location.begin, int))
        self.assertTrue(isinstance(location.end, int))
        self.assertEqual(self.BEGIN, location.begin)
        self.assertEqual(self.END, location.end)

    def test_parse_single_location(self):
        location_string = self.SINGLE_LOCATION_STRING
        location = Location.parse(location_string)
        self.assertTrue(isinstance(location.begin, int))
        self.assertTrue(isinstance(location.end, int))
        self.assertEqual(self.BEGIN, location.begin)
        self.assertEqual(self.BEGIN, location.end)

    def test_location_to_dict(self):
        location = Location(self.BEGIN, self.END)
        expected_dictionary = {
            'begin': self.BEGIN,
            'end': self.END,
        }
        self.assertEqual(expected_dictionary, location.to_dict())

    def test_range_location_to_str(self):
        location = Location(self.BEGIN, self.BEGIN)
        self.assertEqual(self.SINGLE_LOCATION_STRING, str(location))

    def test_single_location_to_str(self):
        location = Location(self.BEGIN, self.END)
        self.assertEqual(self.RANGE_LOCATION_STRING, str(location))

    def test_equality_same_values(self):
        l1 = Location(self.BEGIN, self.END)
        l2 = Location(self.BEGIN, self.END)
        self.assertFalse(l1 is l2)
        self.assertTrue(l1 == l2)

    def test_equality_different_values(self):
        l1 = Location(self.BEGIN, self.END)
        l2 = Location(self.BEGIN, self.END + 1)
        self.assertFalse(l1 == l2)

        l2 = Location(self.BEGIN + 1, self.END)
        self.assertFalse(l1 == l2)

    def test_equality_different_types(self):
        l1 = Location(self.BEGIN, self.END)
        l2 = (self.BEGIN, self.END)
        self.assertFalse(l1 == l2)


class MetadataTest(unittest.TestCase):

    def test_create_metadata(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime.now()
        page = 1

        metadata = Metadata(category, location, timestamp, page)

        self.assertEqual(metadata.category, category)
        self.assertEqual(metadata.location, location)
        self.assertEqual(metadata.timestamp, timestamp)
        self.assertEqual(metadata.page, page)

    def test_metadata_to_str_without_page(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)

        metadata = Metadata(category, location, timestamp, page=None)

        # Note the zero-padding in the hour!
        # This means the generated string can differ by a character,
        # but it shouldn't be an issue...
        expected_string = ('- Your Highlight on Location 1-2 | '
                           'Added on Tuesday, September 13, 2016 07:29:09 AM')
        self.assertEqual(expected_string, str(metadata))

    def test_metadata_to_str_with_page(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)
        page = 95

        metadata = Metadata(category, location, timestamp, page)

        expected_string = ('- Your Highlight on page 95 | Location 1-2 | '
                           'Added on Tuesday, September 13, 2016 07:29:09 AM')
        self.assertEqual(expected_string, str(metadata))

    def test_metadata_to_dict(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime.now()
        page = 1

        expected_dict = {
            'category': category,
            'location': {'begin': 1, 'end': 2},
            'page': page,
            'timestamp': timestamp,
        }

        metadata = Metadata(category, location, timestamp, page)
        self.assertEqual(expected_dict, metadata.to_dict())

    def test_parse_metadata_without_page(self):
        metadata_string = ('- Your Highlight on Location 20-21 | '
                           'Added on Tuesday, September 13, 2016 7:29:09 AM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual('Highlight', metadata.category)
        self.assertEqual(Location(20, 21), metadata.location)
        self.assertEqual(datetime.datetime(2016, 9, 13, 7, 29, 9),
                         metadata.timestamp)
        self.assertEqual(None, metadata.page)

    def test_parse_metadata_with_page(self):
        metadata_string = ('- Your Highlight on page 95 | Location 1261-1265 | '
                          'Added on Thursday, July 14, 2016 11:35:52 PM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual('Highlight', metadata.category)
        self.assertEqual(Location(1261, 1265), metadata.location)
        self.assertEqual(datetime.datetime(2016, 7, 14, 23, 35, 52),
                         metadata.timestamp)
        self.assertTrue(isinstance(metadata.page, int))
        self.assertEqual(95, metadata.page)

    def test_parse_metadata_with_single_location(self):
        metadata_string = ('- Your Note on Location 20 | '
                          'Added on Tuesday, September 13, 2016 7:29:09 AM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual('Note', metadata.category)
        self.assertEqual(Location(20, 20), metadata.location)
        self.assertEqual(datetime.datetime(2016, 9, 13, 7, 29, 9),
                         metadata.timestamp)
        self.assertEqual(None, metadata.page)
