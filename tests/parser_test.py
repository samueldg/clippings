import datetime
import json
import os.path
import unittest
from unittest import mock

from clippings.parser import Clipping
from clippings.parser import Document
from clippings.parser import Location
from clippings.parser import Metadata
from clippings.parser import as_dicts
from clippings.parser import as_json
from clippings.parser import as_kindle
from clippings.parser import parse_clippings


class DefaultObjectFactoryMixin:

    object_class = NotImplemented

    defaults = NotImplemented

    @classmethod
    def get_default_object(cls, **kwargs):
        """Return an object with the class defaults as arguments.
        Any kwarg will be used to overwrite these defaults.

        A class using this needs to have two class attributes:
          - object_class: the class to instantiate
          - defaults: default kwargs that will be passed to the class __init__.
        """

        params = cls.defaults.copy()
        params.update(kwargs)
        return cls.object_class(**params)


class DocumentTest(unittest.TestCase, DefaultObjectFactoryMixin):

    object_class = Document

    defaults = {
        'title': '1984',
        'authors': 'George Orwell',
    }

    default_object_string = '1984 (George Orwell)'

    def test_create_document(self):
        document = self.get_default_object()
        self.assertEqual(self.defaults['title'], document.title)
        self.assertEqual(self.defaults['authors'], document.authors)

    def test_parse_document(self):
        document = Document.parse(self.default_object_string)
        self.assertEqual(self.defaults['authors'], document.authors)
        self.assertEqual(self.defaults['title'], document.title)

    def test_document_to_string(self):
        document = self.get_default_object()
        self.assertEqual(self.default_object_string, str(document))

    def test_document_to_dict(self):
        document = self.get_default_object()
        self.assertEqual(self.defaults, document.to_dict())

    def test_equality_same_values(self):
        document1 = self.get_default_object()
        document2 = self.get_default_object()
        self.assertFalse(document1 is document2)
        self.assertEqual(document1, document2)

    def test_equality_different_values(self):
        document1 = self.get_default_object()
        document2 = self.get_default_object(authors='Lewis Carroll')
        self.assertNotEqual(document1, document2)

    def test_equality_different_types(self):
        document = self.get_default_object()
        not_a_document = self.defaults
        self.assertNotEqual(document, not_a_document)


class LocationTest(unittest.TestCase, DefaultObjectFactoryMixin):

    object_class = Location

    defaults = {
        'begin': 666,
        'end': 1337,
    }

    single_location_string = '666'

    range_location_string = '666-1337'

    def test_create_location(self):
        location = self.get_default_object()
        self.assertEqual(self.defaults['begin'], location.begin)
        self.assertEqual(self.defaults['end'], location.end)

    def test_parse_range_location(self):
        location_string = self.range_location_string
        location = Location.parse(location_string)
        self.assertEqual(self.defaults['begin'], location.begin)
        self.assertEqual(self.defaults['end'], location.end)

    def test_parse_single_location(self):
        location_string = self.single_location_string
        location = Location.parse(location_string)
        self.assertEqual(self.defaults['begin'], location.begin)
        self.assertEqual(self.defaults['begin'], location.end)

    def test_location_to_dict(self):
        location = self.get_default_object()
        self.assertEqual(self.defaults, location.to_dict())

    def test_range_location_to_str(self):
        location = self.get_default_object()
        self.assertEqual(self.range_location_string, str(location))

    def test_single_location_to_str(self):
        location = self.get_default_object(end=self.defaults['begin'])
        self.assertEqual(self.single_location_string, str(location))

    def test_equality_same_values(self):
        location1 = self.get_default_object()
        location2 = self.get_default_object()
        self.assertFalse(location1 is location2)
        self.assertEqual(location1, location2)

    def test_equality_different_values(self):
        location1 = self.get_default_object()
        location2 = self.get_default_object(end=self.defaults['end'] + 1)
        self.assertNotEqual(location1, location2)

    def test_equality_different_types(self):
        location = self.get_default_object()
        not_a_location = self.defaults
        self.assertNotEqual(location, not_a_location)


class MetadataTest(unittest.TestCase, DefaultObjectFactoryMixin):

    object_class = Metadata

    defaults = {
        'category': 'Highlight',
        'location': LocationTest.get_default_object(),
        'page': 95,
        'timestamp': datetime.datetime(2016, 9, 13, 7, 29, 9),
    }

    def test_create_metadata(self):
        metadata = self.get_default_object()
        self.assertEqual(self.defaults['category'], metadata.category)
        self.assertEqual(self.defaults['location'], metadata.location)
        self.assertEqual(self.defaults['page'], metadata.page)
        self.assertEqual(self.defaults['timestamp'], metadata.timestamp)

    def test_metadata_to_str_without_page(self):
        metadata = self.get_default_object(page=None)
        expected_string = ('- Your Highlight on Location 666-1337 | '
                           'Added on Tuesday, September 13, 2016 7:29:09 AM')
        self.assertEqual(expected_string, str(metadata))

    def test_metadata_to_str_with_page(self):
        metadata = self.get_default_object()
        expected_string = ('- Your Highlight on page 95 | Location 666-1337 | '
                           'Added on Tuesday, September 13, 2016 7:29:09 AM')
        self.assertEqual(expected_string, str(metadata))

    def test_metadata_to_dict(self):
        metadata = self.get_default_object()
        expected_dict = self.defaults.copy()
        expected_dict['location'] = expected_dict['location'].to_dict()
        self.assertEqual(expected_dict, metadata.to_dict())

    def test_parse_metadata_without_page(self):
        metadata_string = ('- Your Highlight on Location 666-1337 | '
                           'Added on Tuesday, September 13, 2016 7:29:09 AM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual(self.defaults['category'], metadata.category)
        self.assertEqual(self.defaults['location'], metadata.location)
        self.assertEqual(self.defaults['timestamp'], metadata.timestamp)
        self.assertEqual(None, metadata.page)

    def test_parse_metadata_with_page(self):
        metadata_string = ('- Your Highlight on page 95 | Location 666-1337 | '
                           'Added on Thursday, September 13, 2016 7:29:09 AM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual(self.defaults['category'], metadata.category)
        self.assertEqual(self.defaults['location'], metadata.location)
        self.assertEqual(self.defaults['timestamp'], metadata.timestamp)
        self.assertEqual(self.defaults['page'], metadata.page)

    def test_parse_metadata_with_single_location(self):
        metadata_string = ('- Your Note on Location 20 | '
                           'Added on Tuesday, September 13, 2016 7:29:09 AM')
        metadata = Metadata.parse(metadata_string)

        self.assertEqual('Note', metadata.category)
        self.assertEqual(self.defaults['timestamp'], metadata.timestamp)
        self.assertEqual(Location(20, 20), metadata.location)
        self.assertEqual(None, metadata.page)

    def test_equality_same_values(self):
        metadata1 = self.get_default_object()
        metadata2 = self.get_default_object()
        self.assertFalse(metadata1 is metadata2)
        self.assertEqual(metadata1, metadata2)

    def test_equality_different_values(self):
        metadata1 = self.get_default_object()
        metadata2 = self.get_default_object(page=None)
        self.assertNotEqual(metadata1, metadata2)

    def test_equality_different_types(self):
        metadata = self.get_default_object()
        not_a_metadata = self.defaults
        self.assertNotEqual(metadata, not_a_metadata)


class ClippingTest(unittest.TestCase, DefaultObjectFactoryMixin):

    object_class = Clipping

    defaults = {
        'document': DocumentTest.get_default_object(),
        'metadata': MetadataTest.get_default_object(),
        'content': 'Some \n content'
    }

    def test_create_clipping(self):
        clipping = self.get_default_object()
        self.assertEqual(self.defaults['document'], clipping.document)
        self.assertEqual(self.defaults['metadata'], clipping.metadata)
        self.assertEqual(self.defaults['content'], clipping.content)

    def test_clipping_to_str(self):
        document = mock.MagicMock()
        document.__str__ = mock.MagicMock(return_value='Title (Author)')
        metadata = mock.MagicMock()
        metadata.__str__ = mock.MagicMock(return_value='SO META!')
        content = 'Some content'

        expected_string = "Title (Author)\nSO META!\nSome content"

        clipping = Clipping(document, metadata, content)
        self.assertEqual(expected_string, str(clipping))

    def test_clipping_to_dict(self):
        document = mock.MagicMock()
        document.to_dict = mock.MagicMock(return_value={'doc': 'ument'})
        metadata = mock.MagicMock()
        metadata.to_dict = mock.MagicMock(return_value={'meta': 'data'})
        content = 'Some content'

        expected_dict = {
            'content': 'Some content',
            'document': {'doc': 'ument'},
            'metadata': {'meta': 'data'},
        }

        clipping = Clipping(document, metadata, content)
        self.assertEqual(expected_dict, clipping.to_dict())

    def test_equality_same_values(self):
        clipping1 = self.get_default_object()
        clipping2 = self.get_default_object()
        self.assertFalse(clipping1 is clipping2)
        self.assertEqual(clipping1, clipping2)

    def test_equality_different_values(self):
        clipping1 = self.get_default_object()
        clipping2 = self.get_default_object(content='Different')
        self.assertNotEqual(clipping1, clipping2)

    def test_equality_different_types(self):
        clipping = self.get_default_object()
        not_a_clipping = self.defaults
        self.assertNotEqual(clipping, not_a_clipping)


class ClippingFileParsingTest(unittest.TestCase):

    test_resources_dir = os.path.join('tests', 'resources')

    @property
    def maxDiff(self):
        """See the full diff upon failure, for these tests."""
        return None

    def test_parse_clippings_file_to_json(self):

        clippings = self._parse_sample_clippings_file()

        results_file_path = os.path.join(self.test_resources_dir, 'clippings.json')
        with open(results_file_path) as results_file:
            expected_results = json.load(results_file)
        actual_results = as_json(clippings)
        actual_results = json.loads(actual_results)
        self.assertEqual(expected_results, actual_results)

    def test_parse_clippings_file_to_kindle(self):

        clippings = self._parse_sample_clippings_file()

        # Parse the Kindle file, then regenerate it, and compare.
        results_file_path = os.path.join(self.test_resources_dir, 'clippings.txt')
        with open(results_file_path) as results_file:
            expected_results = results_file.read()
        actual_results = as_kindle(clippings)
        self.assertEqual(expected_results, actual_results)

    def test_parse_clippings_file_to_dict(self):

        clippings = self._parse_sample_clippings_file()

        # Compare the actual results against a JSON of expected results
        results_file_path = os.path.join(self.test_resources_dir, 'clippings.dict')
        with open(results_file_path) as results_file:
            expected_results = eval(results_file.read())
        actual_results = as_dicts(clippings)
        self.assertEqual(expected_results, actual_results)

    def _parse_sample_clippings_file(self):
        """Parse the clippings.txt file in the test resources, and returns
        the list of Clipping objects.

        In the process, we validate the correct number of clippings were parsed,
        so test failures are caught early."""

        clippings_file_path = os.path.join(self.test_resources_dir, 'clippings.txt')

        with open(clippings_file_path, 'r') as clippings_file:
            clippings = parse_clippings(clippings_file)

        self.assertIsNotNone(clippings)
        self.assertEqual(5, len(clippings), '5 clippings should be parsed!')

        return clippings
