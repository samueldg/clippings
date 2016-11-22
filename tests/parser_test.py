import datetime
import unittest

from unittest.mock import MagicMock

from clippings.parser import Clipping
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

    def test_equality_same_values(self):
        title = 'Alice\'s Adventures in Wonderland,'
        authors = ['Lewis Carroll']
        document1 = Document(title, authors)
        document2 = Document(title, authors)

        self.assertFalse(document1 is document2)
        self.assertEqual(document1, document2)

    def test_equality_different_values(self):
        title = 'Alice\'s Adventures in Wonderland,'
        authors = ['Lewis Carroll']
        document1 = Document(title, authors)
        document2 = Document(title, ['Louise Carole'])

        self.assertNotEqual(document1, document2)

    def test_equality_different_types(self):
        title = 'Alice\'s Adventures in Wonderland,'
        authors = ['Lewis Carroll']
        document1 = Document(title, authors)
        document2 = (title, authors)
        self.assertNotEqual(document1, document2)


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
        expected_dict = {
            'begin': self.BEGIN,
            'end': self.END,
        }
        self.assertEqual(expected_dict, location.to_dict())

    def test_range_location_to_str(self):
        location = Location(self.BEGIN, self.BEGIN)
        self.assertEqual(self.SINGLE_LOCATION_STRING, str(location))

    def test_single_location_to_str(self):
        location = Location(self.BEGIN, self.END)
        self.assertEqual(self.RANGE_LOCATION_STRING, str(location))

    def test_equality_same_values(self):
        location1 = Location(self.BEGIN, self.END)
        location2 = Location(self.BEGIN, self.END)
        self.assertFalse(location1 is location2)
        self.assertEqual(location1, location2)

    def test_equality_different_values(self):
        location1 = Location(self.BEGIN, self.END)
        location2 = Location(self.BEGIN, self.END + 1)
        self.assertNotEqual(location1, location2)

        location2 = Location(self.BEGIN + 1, self.END)
        self.assertNotEqual(location1, location2)

    def test_equality_different_types(self):
        location1 = Location(self.BEGIN, self.END)
        location2 = (self.BEGIN, self.END)
        self.assertNotEqual(location1, location2)


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

    def test_equality_same_values(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)

        metadata1 = Metadata(category, location, timestamp, page=None)
        metadata2 = Metadata(category, location, timestamp, page=None)

        self.assertFalse(metadata1 is metadata2)
        self.assertEqual(metadata1, metadata2)

    def test_equality_different_values(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)

        metadata1 = Metadata(category, location, timestamp, page=None)
        metadata2 = Metadata(category, location, timestamp, page=1)

        self.assertNotEqual(metadata1, metadata2)

    def test_equality_different_types(self):
        category = 'Highlight'
        location = Location(1, 2)
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)

        metadata1 = Metadata(category, location, timestamp, page=None)
        metadata2 = (category, location, timestamp, None)

        self.assertNotEqual(metadata1, metadata2)


class ClippingTest(unittest.TestCase):

    def test_create_clipping(self):
        document = MagicMock()
        metadata = MagicMock()
        content = 'Some content'

        clipping = Clipping(document, metadata, content)

        self.assertEqual(document, clipping.document)
        self.assertEqual(metadata, clipping.metadata)
        self.assertEqual(content, clipping.content)

    def test_clipping_to_str(self):
        document = MagicMock()
        document.__str__ = MagicMock(return_value='Title (Author)')
        metadata = MagicMock()
        metadata.__str__ = MagicMock(return_value='SO META!')
        content = 'Some content'

        expected_string = "Title (Author)\nSO META!\nSome content"

        clipping = Clipping(document, metadata, content)
        self.assertEqual(expected_string, str(clipping))

    def test_clipping_to_dict(self):
        document = MagicMock()
        document.to_dict = MagicMock(return_value={'doc': 'ument'})
        metadata = MagicMock()
        metadata.to_dict = MagicMock(return_value={'meta': 'data'})
        content = 'Some content'

        expected_dict = {
            'content': 'Some content',
            'document': {'doc': 'ument'},
            'metadata': {'meta': 'data'},
        }

        clipping = Clipping(document, metadata, content)
        self.assertEqual(expected_dict, clipping.to_dict())

    def test_equality_same_values(self):
        document = Document('Title', ['Author'])
        location = Location(1, 2)
        category = 'Note'
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)
        metadata = Metadata(category, location, timestamp)
        content = 'Nothing much here'

        clipping1 = Clipping(document, metadata, content)
        clipping2 = Clipping(document, metadata, content)

        self.assertFalse(clipping1 is clipping2)
        self.assertEqual(clipping1, clipping2)

    def test_equality_different_values(self):
        document = Document('Title', ['Author'])
        location = Location(1, 2)
        category = 'Note'
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)
        metadata = Metadata(category, location, timestamp)
        content = 'Nothing much here'

        clipping1 = Clipping(document, metadata, content)
        clipping2 = Clipping(document, metadata, content + '!')

        self.assertNotEqual(clipping1, clipping2)

    def test_equality_different_types(self):
        document = Document('Title', ['Author'])
        location = Location(1, 2)
        category = 'Note'
        timestamp = datetime.datetime(2016, 9, 13, 7, 29, 9)
        metadata = Metadata(category, location, timestamp)
        content = 'Nothing much here'

        clipping1 = Clipping(document, metadata, content)
        clipping2 = (document, metadata, content)

        self.assertNotEqual(clipping1, clipping2)
