import subprocess
import json

ENDPOINT = "https://api.tdameritrade.com/v1/marketdata/chains"

# ------------------------------
# This class defines the Exception that gets thrown when the api input is bad.
class API_InputError(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

# ------------------------------
# This function verifies that the required apikey and symbol arguments are provided.
def _test_input(*args, **kwargs):
    if ("apikey" not in kwargs.keys()) or ("symbol" not in kwargs.keys()):
        raise API_InputError("Bad input. `apikey` and `symbol` are required.")

def get(*args, **kwargs):
    """Request an option chain from TDAmeritrade's API.

    Args:
        apikey (str):            API key to api.tdameritrade.com.
        symbol (str):            Stock symbol to get the option chain for.
        contractType (str):      Type of contracts to return in the chain. Can be CALL, PUT, or ALL. Default is ALL.
        strikeCount (int):       The number of strikes to return above and below the at-the-money price.
        includeQuotes (str):     Include quotes for options in the option chain. Can be TRUE or FALSE. Default is FALSE.
        strategy (str):          Passing a value returns a Strategy Chain. Default is SINGLE.
        interval (int):          Strike interval for spread strategy chains.
        strike (int):            Provide a strike price to return options only at that strike price.
        range (str):             Returns options for the given range. Default is ALL.
        fromDate (str):          Only return expirations after this date.
        toDate (str):            Only return expirations before this date.
        volatility (float):      Volatility to use in calculations. Applies only to ANALYTICAL strategy chains.
        underlyingPrice (float): Underlying price to use in calculations. Applies only to ANALYTICAL strategy chains.
        interestRate (float):    Interest rate to use in calculations. Applies only to ANALYTICAL strategy chains.
        daysToExpiration (int):  Days to expiration to use in calculations. Applies only to ANALYTICAL strategy chains.
        expMonth (str):          Return only options expiring in the specified month. Example: JAN. Default is ALL.
        optionType (str):        Type of contracts to return. Default is ALL.

    Returns:
        resp (dict): API response with option chain.
    """
    _test_input(*args, **kwargs)

    url = "?".join([ENDPOINT, "&".join(f"{k}={v}" for k, v in kwargs.items())])
    resp = json.loads(subprocess.check_output(["curl", "-gs", url]))
    if resp.get("error"):
        raise API_InputError("Bad query. Contains unknown query parameters.")

    return resp
