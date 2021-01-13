from unittest import mock

from clippings.parser import main as parser_main

from .utils.context import cli_args


def test_output_format_json(capsys):
    with cli_args(['tests/resources/clippings.txt', '-o', 'json']), \
         mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock:

        parser_main()

    as_json_mock.assert_called_once()
    assert capsys.readouterr().out == '{"j": "son"}'


def test_output_format_dict(capsys):
    with cli_args(['tests/resources/clippings.txt', '-o', 'dict']), \
         mock.patch('clippings.parser.as_dicts', return_value={'d': 'ict'}) as as_dicts_mock:

        parser_main()

    as_dicts_mock.assert_called_once()
    assert capsys.readouterr().out == str({'d': 'ict'})


def test_output_format_kindle(capsys):
    with cli_args(['tests/resources/clippings.txt', '-o', 'kindle']), \
         mock.patch('clippings.parser.as_kindle', return_value='kindle') as as_kindle_mock:

        parser_main()

    as_kindle_mock.assert_called_once()
    assert capsys.readouterr().out == 'kindle'


def test_output_format_defaults_to_json(capsys):
    with cli_args(['tests/resources/clippings.txt']), \
         mock.patch('clippings.parser.as_json', return_value='{"j": "son"}') as as_json_mock:

        parser_main()

    as_json_mock.assert_called_once()
    assert capsys.readouterr().out == '{"j": "son"}'
