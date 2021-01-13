import datetime
import json

import pytest

from clippings.utils import DatetimeJSONEncoder


DATE = datetime.datetime(2016, 1, 2, 3, 4, 5)
DATE_STRING = "2016-01-02T03:04:05"


def test_datetime_encoder_format():
    dictionary = {"now": DATE}
    expected_json_string = json.dumps({"now": DATE_STRING})
    json_string = json.dumps(dictionary, cls=DatetimeJSONEncoder)
    assert json_string == expected_json_string


def test_datetime_encoder_typeerror():
    undumpable_dictionary = {"set": set()}
    # Ensure we let the parent raise TypeError
    with pytest.raises(TypeError):
        json.dumps(undumpable_dictionary, cls=DatetimeJSONEncoder)
