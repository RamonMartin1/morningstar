import yaml
import json
import sys

from morningstar.models.ms_response import MSResponse
from morningstar.provider.morningstar import Morningstar
from morningstar.config import config

### FIXED RATE BOND ###
#------------------------
#ISIN = "CH0419042491" # NESTLE, SIX
#EXCHANGE = "182"
#TICKER = "NES18"

### FLOATING RATE BOND WITHOUT IR ###
#-------------------------
#ISIN = "CH0406990827"
#EXCHANGE = "182" 
#TICKER = "SIK181"

ISIN = "CH0384125057"
EXCHANGE = "182" 
TICKER = "CSG2"

STATIC = True
WRITE = True


def write_dict(data: dict, filename: str):
    with open(filename, "w") as f:
        print(json.dumps(data, indent=2), file=f)


def print_dict(data: dict):
    print(json.dumps(data, indent=2), file=sys.stdout)


def get_instruments(provider: Morningstar):
    """
    Search exchange for instruments
    """
    response = provider.search(params={"exchange": EXCHANGE})
    if len(response.results):
        print_dict(response.results[0].data)


def get_exchange(provider: Morningstar):
    """
    Search for instruments and add info about primary exchange
    """
    response = provider.search(params={"isin": ISIN})
    field = "S724"
    query = { "isin": ISIN, "fields": field }
    response2 = provider.index(params=query)
    if len(response2.results):
        response.results[0].data.update(response2.results[0].data)
    print_dict(response.results[0].data)


def query(provider: Morningstar):
    """ 
    Query static/dynamic fields for asset
    """
    if STATIC:
        field = "SA"
        filename = "{}_sv.txt".format(TICKER)
    else:
        field = "DA"
        filename = "{}_dv.txt".format(TICKER)
    query = {
            "isin": ISIN,
            "exchange": EXCHANGE,
            "fields": field
            }
    response = provider.index(params=query)
    if len(response.results):
        if WRITE:
            write_dict(response.results[0].data, filename)
        else: 
            print_dict(response.results[0].data, filename)


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
    if WRITE:
        write_dict(fields, filename)
    else:
        print_dict(fields, filename)


if __name__ == "__main__":
    provider = Morningstar(config=config["provider"]["morningstar"])
    get_exchange(provider)
    query(provider)
    fields(provider)

