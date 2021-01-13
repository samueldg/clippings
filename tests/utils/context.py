import sys
from contextlib import contextmanager
from unittest.mock import patch


@contextmanager
def cli_args(arg_list):
    """Context manager to mock sys.argv to fake the program was called with
    the arguments in arg_list.

    E.g.
        cli_args(['test.txt', '-o', 'dict'])
    Corresponds to :
        python -m clippings.parser test.txt -o dict
    """
    mock_argv = ['clippings.py'] + arg_list
    with patch.object(sys, 'argv', mock_argv):
        yield
