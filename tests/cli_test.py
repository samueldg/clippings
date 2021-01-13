from unittest import mock

from clippings.parser import main as parser_main

from .utils.context import cli_args
from .utils.context import capture_stdout


def test_output_format_json():
    with cli_args(['tests/resources/clippings.txt', '-o', 'json']), \
         mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock, \
         capture_stdout() as stdout:

        parser_main()

    as_json_mock.assert_called_once()
    assert stdout.read() == '{"j": "son"}'


def test_output_format_dict():
    with cli_args(['tests/resources/clippings.txt', '-o', 'dict']), \
         mock.patch('clippings.parser.as_dicts', return_value={'d': 'ict'}) as as_dicts_mock, \
         capture_stdout() as stdout:

        parser_main()

    as_dicts_mock.assert_called_once()
    assert stdout.read() == str({'d': 'ict'})


def test_output_format_kindle():
    with cli_args(['tests/resources/clippings.txt', '-o', 'kindle']), \
         mock.patch('clippings.parser.as_kindle', return_value='kindle') as as_kindle_mock, \
         capture_stdout() as stdout:

        parser_main()

    as_kindle_mock.assert_called_once()
    assert stdout.read() == 'kindle'


def test_output_format_defaults_to_json():
    with cli_args(['tests/resources/clippings.txt']), \
         mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock, \
         capture_stdout() as stdout:

        parser_main()

    as_json_mock.assert_called_once()
    assert stdout.read() == '{"j": "son"}'
