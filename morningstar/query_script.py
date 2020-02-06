import yaml
import json

from morningstar.models.ms_response import MSResponse
from morningstar.provider.morningstar import Morningstar


CONFIG_PATH = "../config-morningstar.yml"
CONFIG = yaml.safe_load(open(CONFIG_PATH))['provider']['morningstar']


def print_response(ms: MSResponse):
    n = len(ms.results)
    for i in range(n):
        print(json.dumps(ms.results[i].data, indent=2))


def corpactions(provider: Morningstar):
    """
    Directly query corporate actions
    """
    query = {
            "instrument": "151.1.1.VOD",
            "corpactions": True
            }
    response = provider.index_ts(params=query)
    if len(response.results):
        print_response(response)


def query(provider: Morningstar):
    """ 
    Query static/dynamic fields for asset
    """
    query = {
            "isin": "CH0244767585",
            "exchange": "182",
            "fields": "SA"
            }
    response = provider.index(params=query)
    if len(response.results):
        print_response(response)


def fields(provider: Morningstar):
    """
    Query field IDs by querying each fields
    """
    N = 4397; letter = "D"; filename = "dynamic_fields.txt"
    # N = 5274; letter = "S"; filename = "static_fields.txt"
    fields = {}
    for i in range(N):
        field = letter + str(i)
        query = {
                "isin": "CH0244767585",
                "exchange": "182",
                "fields": field
                }
        response = provider.index(params=query)
        if len(response.results):
            key = list(response.results[0].data.keys())[0]
            fields[key] = field
            print("{}: {}".format(key, field))
    with open(filename, "w") as f:
        print(json.dumps(fields, indent=2), file=f)



if __name__ == "__main__":
    provider = Morningstar(config=CONFIG)
    # query(provider)
    fields(provider)


