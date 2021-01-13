import datetime
import json
import os.path
import unittest
from copy import deepcopy
from unittest.mock import Mock

import pytest

from clippings.parser import Clipping
from clippings.parser import Document
from clippings.parser import Location
from clippings.parser import Metadata
from clippings.parser import as_dicts
from clippings.parser import as_json
from clippings.parser import as_kindle
from clippings.parser import parse_clippings


TEST_RESOURCES_DIR = os.path.join('tests', 'resources')


@pytest.fixture(name='document_title')
def fixture_document_title():
    return '1984'


@pytest.fixture(name='document_authors')
def fixture_document_authors():
    return 'George Orwell'


@pytest.fixture(name='document')
def fixture_document(document_title, document_authors):
    return Document(
        title=document_title,
        authors=document_authors,
    )


@pytest.fixture(name='document_as_str')
def fixture_document_as_str():
    return '1984 (George Orwell)'


@pytest.fixture(name='document_as_dict')
def fixture_document_as_dict(document_title, document_authors):
    return {
        'title': document_title,
        'authors': document_authors,
    }


def test_create_document(document, document_title, document_authors):
    assert document.title == document_title
    assert document.authors == document_authors


def test_parse_document(document_as_str, document_title, document_authors):
    document = Document.parse(document_as_str)
    assert document.authors == document_authors
    assert document.title == document_title


def test_document_to_string(document, document_as_str):
    assert str(document) == document_as_str


def test_document_to_dict(document, document_as_dict):
    assert document.to_dict() == document_as_dict


def test_document_equality_same_values(document, document_as_dict):
    other_document = Document(**document_as_dict)
    assert other_document is not document
    assert other_document == document


def test_document_equality_different_values(document, document_as_dict):
    other_document_kwargs = deepcopy(document_as_dict)
    other_document_kwargs['authors'] = 'Lewis Carroll'
    other_document = Document(**other_document_kwargs)
    assert other_document != document


def test_document_equality_different_types(document, document_as_dict):
    assert document != document_as_dict
    assert document_as_dict != document


@pytest.fixture(name='location_begin')
def fixture_location_begin():
    return 666


@pytest.fixture(name='location_end')
def fixture_location_end():
    return 1337


@pytest.fixture(name='location_range')
def fixture_location_range(location_begin, location_end):
    return Location(
        begin=location_begin,
        end=location_end,
    )


@pytest.fixture(name='location_single')
def fixture_location_single(location_begin):
    return Location(
        begin=location_begin,
        end=location_begin,
    )


@pytest.fixture(name='location_range_as_str')
def fixture_location_range_as_str():
    return '666-1337'


@pytest.fixture(name='location_single_as_str')
def fixture_location_single_as_str(location_begin):
    return '666'


@pytest.fixture(name='location_range_as_dict')
def fixture_location_range_as_dict(location_begin, location_end):
    return {
        'begin': location_begin,
        'end': location_end,
    }


def test_create_location(location_range, location_begin, location_end):
    assert location_range.begin == location_begin
    assert location_range.end == location_end


def test_parse_range_location(location_range_as_str, location_begin, location_end):
    location = Location.parse(location_range_as_str)
    assert location.begin == location_begin
    assert location.end == location_end


def test_parse_single_location(location_single_as_str, location_begin):
    location = Location.parse(location_single_as_str)
    assert location.begin == location_begin
    assert location.end == location_begin


def test_location_to_dict(location_range, location_range_as_dict):
    assert location_range.to_dict() == location_range_as_dict


def test_range_location_to_str(location_range, location_range_as_str):
    assert str(location_range) == location_range_as_str


def test_single_location_to_str(location_single, location_single_as_str):
    assert str(location_single) == location_single_as_str


def test_location_equality_same_values(location_range, location_range_as_dict):
    other_location = Location(**location_range_as_dict)
    assert other_location is not location_range
    assert other_location == location_range


def test_location_equality_different_values(location_range, location_range_as_dict):
    other_location_kwargs = deepcopy(location_range_as_dict)
    other_location_kwargs['end'] += 1
    other_location = Location(**other_location_kwargs)
    assert other_location != location_range


def test_location_equality_different_types(location_range, location_range_as_dict):
    assert location_range != location_range_as_dict
    assert location_range_as_dict != location_range


@pytest.fixture(name='category')
def fixture_category():
    return 'Highlight'


@pytest.fixture(name='page')
def fixture_page():
    return 95


@pytest.fixture(name='timestamp')
def fixture_timestamp():
    return datetime.datetime(2016, 9, 13, 7, 29, 9)


@pytest.fixture(name='metadata')
def fixture_metadata(category, location_range, page, timestamp):
    return Metadata(
        category=category,
        location=location_range,
        page=page,
        timestamp=timestamp,
    )


@pytest.fixture(name='metadata_as_dict')
def fixture_metadata_as_dict(category, location_range_as_dict, page, timestamp):
    return {
        'category': category,
        'location': location_range_as_dict,
        'page': page,
        'timestamp': timestamp,
    }


def test_create_metadata(metadata, category, location_range, page, timestamp):
    assert metadata.category == category
    assert metadata.location == location_range
    assert metadata.page == page
    assert metadata.timestamp == timestamp


def test_metadata_to_str_with_page(metadata):
    expected_string = ('- Your Highlight on page 95 | Location 666-1337 | '
                       'Added on Tuesday, September 13, 2016 7:29:09 AM')
    assert str(metadata) == expected_string


@pytest.mark.parametrize('page', [None])
def test_metadata_to_str_without_page(metadata):
    expected_string = ('- Your Highlight on Location 666-1337 | '
                       'Added on Tuesday, September 13, 2016 7:29:09 AM')
    assert str(metadata) == expected_string


def test_metadata_to_dict(metadata, metadata_as_dict):
    assert metadata.to_dict() == metadata_as_dict


def test_parse_metadata_without_page(category, location_range, timestamp):
    metadata_string = ('- Your Highlight on Location 666-1337 | '
                       'Added on Tuesday, September 13, 2016 7:29:09 AM')
    metadata = Metadata.parse(metadata_string)

    assert metadata.category == category
    assert metadata.location == location_range
    assert metadata.timestamp == timestamp
    assert metadata.page is None


def test_parse_metadata_with_page(category, location_range, timestamp, page):
    metadata_string = ('- Your Highlight on page 95 | Location 666-1337 | '
                       'Added on Thursday, September 13, 2016 7:29:09 AM')
    metadata = Metadata.parse(metadata_string)

    assert metadata.category == category
    assert metadata.location == location_range
    assert metadata.timestamp == timestamp
    assert metadata.page == page


def test_parse_metadata_with_single_location(timestamp, page):
    metadata_string = ('- Your Note on Location 20 | '
                       'Added on Tuesday, September 13, 2016 7:29:09 AM')
    metadata = Metadata.parse(metadata_string)

    assert metadata.category == 'Note'
    assert metadata.timestamp == timestamp
    assert metadata.location == Location(20, 20)
    assert metadata.page is None


def test_metadata_equality_same_values(metadata, category, location_range, page, timestamp):
    other_metadata = Metadata(
        category=category,
        location=location_range,
        page=page,
        timestamp=timestamp,
    )
    assert other_metadata is not metadata
    assert other_metadata == metadata


def test_metadata_equality_different_values(metadata, category, location_range, timestamp):
    other_metadata = Metadata(
        category=category,
        location=location_range,
        page=None,
        timestamp=timestamp,
    )
    assert other_metadata != metadata


def test_metadata_equality_different_types(metadata, metadata_as_dict):
    assert metadata != metadata_as_dict


@pytest.fixture(name='content')
def fixture_content():
    'Some \n content'


@pytest.fixture(name='clipping')
def fixture_clipping(document, metadata, content):
    return Clipping(
        document=document,
        metadata=metadata,
        content=content,
    )


def test_create_clipping(clipping, document, metadata, content):
    assert clipping.document == document
    assert clipping.metadata == metadata
    assert clipping.content == content


def test_clipping_to_str():
    document = Mock()
    document.__str__ = Mock(return_value='Title (Author)')
    metadata = Mock()
    metadata.__str__ = Mock(return_value='SO META!')
    content = 'Some content'
    clipping = Clipping(document, metadata, content)

    expected_string = "Title (Author)\nSO META!\nSome content"

    assert str(clipping) == expected_string


def test_clipping_to_dict():
    document = Mock()
    document.to_dict = Mock(return_value={'doc': 'ument'})
    metadata = Mock()
    metadata.to_dict = Mock(return_value={'meta': 'data'})
    content = 'Some content'
    clipping = Clipping(document, metadata, content)

    expected_dict = {
        'content': 'Some content',
        'document': {'doc': 'ument'},
        'metadata': {'meta': 'data'},
    }

    assert clipping.to_dict() == expected_dict


def test_clipping_equality_same_values(clipping, document, metadata, content):
    other_clipping = Clipping(
        document=document,
        metadata=metadata,
        content=content,
    )

    assert other_clipping is not clipping
    assert other_clipping == clipping


def test_clipping_equality_different_values(clipping, document, metadata):
    other_clipping = Clipping(
        document=document,
        metadata=metadata,
        content='Different content',
    )

    assert other_clipping != clipping


def test_clipping_equality_different_types(clipping):
    assert clipping != clipping.to_dict()


class ClippingFileParsingTest(unittest.TestCase):

    @property
    def maxDiff(self):
        """See the full diff upon failure, for these tests."""
        return None

    def test_parse_clippings_file_to_json(self):

        clippings = self._parse_sample_clippings_file()

        results_file_path = os.path.join(TEST_RESOURCES_DIR, 'clippings.json')
        with open(results_file_path) as results_file:
            expected_results = json.load(results_file)
        actual_results = as_json(clippings)
        actual_results = json.loads(actual_results)
        self.assertEqual(expected_results, actual_results)

    def test_parse_clippings_file_to_kindle(self):

        clippings = self._parse_sample_clippings_file()

        # Parse the Kindle file, then regenerate it, and compare.
        results_file_path = os.path.join(TEST_RESOURCES_DIR, 'clippings.txt')
        with open(results_file_path) as results_file:
            expected_results = results_file.read()
        actual_results = as_kindle(clippings)
        self.assertEqual(expected_results, actual_results)

    def test_parse_clippings_file_to_dict(self):

        clippings = self._parse_sample_clippings_file()

        # Compare the actual results against a JSON of expected results
        results_file_path = os.path.join(TEST_RESOURCES_DIR, 'clippings.dict')
        with open(results_file_path) as results_file:
            expected_results = eval(results_file.read())
        actual_results = as_dicts(clippings)
        self.assertEqual(expected_results, actual_results)

    def _parse_sample_clippings_file(self):
        """Parse the clippings.txt file in the test resources, and returns
        the list of Clipping objects.

        In the process, we validate the correct number of clippings were parsed,
        so test failures are caught early."""

        clippings_file_path = os.path.join(TEST_RESOURCES_DIR, 'clippings.txt')

        with open(clippings_file_path, 'r') as clippings_file:
            clippings = parse_clippings(clippings_file)

        self.assertIsNotNone(clippings)
        self.assertEqual(5, len(clippings), '5 clippings should be parsed!')

        return clippings
