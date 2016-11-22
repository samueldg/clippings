"""Various utilies not related to parsing per se."""

import datetime
import json


class BasicEqualityMixin:
    """Mixin to facilitate implementing the equality operator

    Subclasses of this will test for equality by checking the type, then
    comparing the attributes dictionary.
    """

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__


class DatetimeJSONEncoder(json.JSONEncoder):
    """JSON ecoder that can handle datetime objects.

    The datatime will be encoded as a string, in ISO format.
    """

    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        else:
            return json.JSONEncoder.default(self, obj)
