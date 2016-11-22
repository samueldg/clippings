import datetime
import json
import unittest

from clippings.utils import DatetimeJSONEncoder


DATE = datetime.datetime(2016, 1, 2, 3, 4, 5)
DATE_STRING = "2016-01-02T03:04:05"


class DatetimeJSONEncoderTest(unittest.TestCase):

    def test_datetime_encoder_format(self):
        dictionary = {"now": DATE}
        expected_json_string = json.dumps({"now": DATE_STRING})
        json_string = json.dumps(dictionary, cls=DatetimeJSONEncoder)
        self.assertEqual(expected_json_string, json_string)

    def test_datetime_encoder_typeerror(self):
        undumpable_dictionary = {"set": set()}
        # Ensure we let the parent raise TypeError
        with self.assertRaises(TypeError):
            json_string = json.dumps(undumpable_dictionary, cls=DatetimeJSONEncoder)
