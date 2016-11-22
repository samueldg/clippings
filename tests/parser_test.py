import unittest

from clippings.parser import Document
from clippings.parser import Location


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
