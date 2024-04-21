import json

from bson import json_util


def oid_json_parse(arg):
    return json.loads(json_util.dumps(arg))