from subprocess import check_output
import json

# ------------------------------
# This class defines the URLs to the implemented endpoints.
class Endpoint:
    CHAIN = "https://api.tdameritrade.com/v1/marketdata/chains"
    HIST = "https://api.tdameritrade.com/v1/marketdata/{0}/pricehistory"

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

# ------------------------------
# This function sends the request to the specified API endpoint.
def _get(endpoint, *args, **kwargs):

    url = "?".join([endpoint, "&".join(f"{k}={v}" for k, v in kwargs.items())])
    if (resp := json.loads(check_output(["curl", "-gs", url]))).get("error"):
        raise API_InputError(f"{0}".format(resp["error"]))

    return resp

def get_chain(*args, **kwargs):
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

    endpoint = Endpoint.CHAIN
    return _get(endpoint, *args, **kwargs)

def get_historical(*args, **kwargs):
    """Request historical price data from TDAmeritrade's API.

    Args:
        apikey (str):                API key to api.tdameritrade.com.
        symbol (str):                Stock symbol to get the option chain for.
        periodType (str):            The type of period to show. Can be day, month, year, or ytd.
        period (int):                The number of periods to show.
        frequencyType (str):         The type of frequency with which a new candle is formed. Can be day, month, year, ytd.
        frequency (str):             The number of the frequencyType to be included in each candle.
        startDate (int):             Start date as milliseconds since epoch.
        endDate (int):               End date as milliseconds since epoch.
        needExtendedHoursData (str): true to return extended hours data, false for regular market hours only.

    Returns:
        resp (dict): API response with historical price data.
    """
    _test_input(*args, **kwargs)

    endpoint = Endpoint.HIST.format(kwargs["symbol"])
    return _get(endpoint, *args, **kwargs)
