import unittest
from unittest import mock

from clippings.parser import main as parser_main

from .utils.context import cli_args
from .utils.context import capture_stdout


class MainFunctionTest(unittest.TestCase):

    def test_output_format_json(self):
        with cli_args(['tests/resources/clippings.txt', '-o', 'json']), \
             mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock, \
             capture_stdout() as stdout:

            parser_main()

        self.assertTrue(as_json_mock.called)
        self.assertEqual('{"j": "son"}', stdout.read())

    def test_output_format_dict(self):
        with cli_args(['tests/resources/clippings.txt', '-o', 'dict']), \
             mock.patch('clippings.parser.as_dicts', return_value={'d': 'ict'}) as as_dicts_mock, \
             capture_stdout() as stdout:

            parser_main()

        self.assertTrue(as_dicts_mock.called)
        self.assertEqual(str({'d': 'ict'}), stdout.read())

    def test_output_format_kindle(self):
        with cli_args(['tests/resources/clippings.txt', '-o', 'kindle']), \
             mock.patch('clippings.parser.as_kindle', return_value='kindle') as as_kindle_mock, \
             capture_stdout() as stdout:

            parser_main()

        self.assertTrue(as_kindle_mock.called)
        self.assertEqual('kindle', stdout.read())

    def test_output_format_defaults_to_json(self):
        with cli_args(['tests/resources/clippings.txt']), \
             mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock, \
             capture_stdout() as stdout:

            parser_main()

        self.assertTrue(as_json_mock.called)
        self.assertEqual('{"j": "son"}', stdout.read())
