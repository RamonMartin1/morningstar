import yaml
import json

from morningstar.models.ms_response import MSResponse
from morningstar.provider.morningstar import Morningstar


CONFIG_PATH = "../../config-morningstar.yml"
CONFIG = yaml.safe_load(open(CONFIG_PATH))['provider']['morningstar']

ISIN = "US46186M4078"
EXCHANGE = "19"
TICKER = "nviv"
STATIC = False


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


def write_dict(data: dict, filename: str):
    with open(filename, "w") as f:
        print(json.dumps(data, indent=2), file=f)


def query(provider: Morningstar):
    """ 
    Query static/dynamic fields for asset
    """
    if STATIC:
        field = "SA"
    else:
        field = "DA"
    query = {
            "isin": ISIN,
            "exchange": EXCHANGE,
            "fields": field
            }
    response = provider.index(params=query)
    filename = "{}_{}.txt".format(TICKER, field.lower())
    write_dict(response.results[0].data, filename)


def fields(provider: Morningstar):
    """
    Query field IDs by querying each fields
    """
    if STATIC:
        N = 5274
        letter = "S"
        filename = "{}_sf.txt".format(TICKER)
    else:
        N = 4397
        letter = "D"
        filename = "{}_df.txt".format(TICKER)
    fields = {}
    for i in range(N):
        field = letter + str(i)
        query = {
                "isin": ISIN,
                "exchange": EXCHANGE,
                "fields": field
                }
        response = provider.index(params=query)
        if len(response.results):
            key = list(response.results[0].data.keys())[0]
            fields[key] = field
            print("{}: {}".format(key, field))
    write_dict(fields, filename)


if __name__ == "__main__":
    provider = Morningstar(config=CONFIG)
    query(provider)
    #fields(provider)


