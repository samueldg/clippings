"""Various utilies not related to parsing per se."""

import datetime
import json

class DatetimeJSONEncoder(json.JSONEncoder):
    """JSON ecoder that can handle datetime objects.

    The datatime will be encoded as a string, in ISO format.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
