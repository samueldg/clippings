import unittest

from clippings.parser import Document


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
