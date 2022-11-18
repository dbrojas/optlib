import datetime
import requests
import os

import logging


logger = logging.getLogger(__name__)

# ------------------------------
# This class defines the Exception that gets thrown when the api input is bad.
class InputError(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

# ------------------------------
# This function gets the API key from env, throws exception if not found.
def _get_env(varname):
    if (apikey := os.environ.get(varname)): return apikey
    raise InputError(f"'{varname}' not found in environment")

# ------------------------------
# This function formats a datetime.datetime object into a compatible date string.
def _format_date(date):
    if not date:
        return None
    elif type(date) == datetime.date:
        return date.strftime("%Y-%m-%d")
    elif type(date) == datetime.datetime:
        return date.strftime("%Y-%m-%d'T'%H:%M:%S%z")
    else:
        raise InputError(f"Date must be of type `datetime.datetime` or `datetime`")

# ------------------------------
# This function sends the request to the specified API endpoint.
def _get(endpoint, params={}):
    if "apikey" not in params:
        params.update({"apikey": _get_env("TDA_API_KEY")})
    r = requests.get(endpoint, params=params)
    r.raise_for_status()
    return r.json()

# ------------------------------
# This function gets data from the /chains endpoint.
def get_chain(
    symbol: str,
    contract_type: str = "ALL",
    strike_count: int = None,
    include_quotes: str = "FALSE",
    strategy: str = "SINGLE",
    interval: int = None,
    strike: int = None,
    range: str = "ALL",
    from_date: str = None,
    to_date: str = None,
    volatility: float = None,
    underlying_price: float = None,
    interest_rate: float = None,
    days_to_expiration: int = None,
    exp_month: str = "ALL",
    option_type: str = "ALL",
    apikey: str = None
):
    """Request an option chain from TDAmeritrade's API.

    Args:
        symbol (str):             Stock symbol to get the option chain for (required).
        contract_type (str):      Type of contracts to return in the chain. Can be CALL, PUT, or ALL. Default is ALL.
        strike_count (int):       The number of strikes to return above and below the at-the-money price.
        include_quotes (str):     Include quotes for options in the option chain. Can be TRUE or FALSE. Default is FALSE.
        strategy (str):           Passing a value returns a Strategy Chain. Default is SINGLE.
        interval (int):           Strike interval for spread strategy chains.
        strike (int):             Provide a strike price to return options only at that strike price.
        range (str):              Returns options for the given range. Default is ALL.
        from_date (str):          Only return expirations after this date.
        to_date (str):            Only return expirations before this date.
        volatility (float):       Volatility to use in calculations. Applies only to ANALYTICAL strategy chains.
        underlying_price (float): Underlying price to use in calculations. Applies only to ANALYTICAL strategy chains.
        interest_rate (float):    Interest rate to use in calculations. Applies only to ANALYTICAL strategy chains.
        days_to_expiration (int): Days to expiration to use in calculations. Applies only to ANALYTICAL strategy chains.
        exp_month (str):          Return only options expiring in the specified month. Example: JAN. Default is ALL.
        option_type (str):        Type of contracts to return. Default is ALL.
        apikey (str):             API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        chain (OptionChain): API response with option chain.
    """
    params = {
        "symbol": symbol,
        "contractType": contract_type,
        "strikeCount": strike_count,
        "includeQuotes": include_quotes,
        "strategy": strategy,
        "interval": interval,
        "strike": strike,
        "range": range,
        "fromDate": _format_date(from_date),
        "toDate": _format_date(to_date),
        "volatility": volatility,
        "underlyingPrice": underlying_price,
        "interestRate": interest_rate,
        "daysToExpiration": days_to_expiration,
        "expMonth": exp_month,
        "optionType": option_type,
        "apikey": apikey
    }

    return _get(
        endpoint="https://api.tdameritrade.com/v1/marketdata/chains",
        params={ k: v for k, v in params.items() if v }
    )

# ------------------------------
# This function gets data from the /pricehistory endpoint.
def get_pricehistory(
    symbol: str,
    period_type: str = "year",
    period: int = 1,
    frequency_type: str = "daily",
    frequency: int = 1,
    start_date: datetime.datetime = None,
    end_date: datetime.datetime = None,
    need_extended_hours_data: bool = False,
    apikey: str = None
):
    """Request pricehistory data from TDAmeritrade's API.

    Args:
        symbol (str):                   Stock symbol to get the option chain for (required).
        period_type (str):              The type of period to show. Can be day, month, year, or ytd.
        period (int):                   The number of periods to show.
        frequency_type (str):           The type of frequency with which a new candle is formed. Can be minute, daily, weekly, monthly.
        frequency (str):                The number of the frequencyType to be included in each candle.
        start_date (int):               Start date as milliseconds since epoch.
        end_date (int):                 End date as milliseconds since epoch.
        need_extended_hours_data (str): true to return extended hours data, false for regular market hours only.
        apikey (str):                   API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        response (dict): API response with historical price data.
    """
    params = {
        "periodType": period_type,
        "period": period,
        "frequencyType": frequency_type,
        "frequency": frequency,
        "startDate": _format_date(start_date),
        "endDate": _format_date(end_date),
        "need_extended_hours_data": "true" if need_extended_hours_data else "false",
        "apikey": apikey
    }

    return _get(
        endpoint=f"https://api.tdameritrade.com/v1/marketdata/{symbol}/pricehistory",
        params={ k: v for k, v in params.items() if v }
    )

# ------------------------------
# This function gets data from the /instruments endpoint.
def get_instrument(
    symbol: str,
    apikey: str = None
):
    """Retrieve instrument fundamental data.

    Args:
        symbol (str):    Stock symbol to get the option chain for (required).
        apikey (str):    API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        response (dict): API response with fundamentals data.
    """
    params = {
        "apikey": apikey
    }

    return _get(
        endpoint=f"https://api.tdameritrade.com/v1/instruments/{symbol}",
        params={ k: v for k, v in params.items() if v }
    )

# ------------------------------
# This function gets data from the /instruments endpoint.
def search_instrument(
    symbol: str,
    projection: str = "symbol-search",
    apikey: str = None
):
    """Search instruments.

    The following search methods are available:

    symbol-search: Retrieve instrument data of a specific symbol or cusip

    symbol-regex:  Retrieve instrument data for all symbols matching regex.
        Example: symbol=XYZ.* will return all symbols beginning with XYZ

    desc-search:   Retrieve instrument data for instruments whose description
        contains the word supplied. Example: symbol=FakeCompany will return
        all instruments with FakeCompany in the description.

    desc-regex:    Search description with full regex support. Example: symbol=XYZ.[A-C]
        returns all instruments whose descriptions contain a word beginning with XYZ
        followed by a character A through C.

    fundamental:   Returns fundamental data for a single instrument specified
        by exact symbol.

    Args:
        symbol (str):     Stock symbol to get the option chain for (required).
        projection (str): One of symbol-search, symbol-regex, desc-search, desc-regex, fundamental.
        apikey (str):     API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        response (dict): API response with fundamentals data.
    """
    params = {
        "apikey": apikey,
        "symbol": symbol,
        "projection": projection
    }

    return _get(
        endpoint="https://api.tdameritrade.com/v1/instruments",
        params={ k: v for k, v in params.items() if v }
    )

# ------------------------------
# This function gets data from the /quotes endpoint.
def get_quote(
    symbol: str,
    apikey: str = None
):
    """Get quote for a symbol.

    Args:
        symbol (str):    Stock symbol to get the option chain for (required).
        apikey (str):    API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        response (dict): API response with price quote.
    """
    params = {
        "symbol": symbol,
        "apikey": apikey
    }

    return _get(
        endpoint=f"https://api.tdameritrade.com/v1/marketdata/{symbol}/quotes",
        params={ k: v for k, v in params.items() if v }
    )

# ------------------------------
# This function gets data from the /movers endpoint.
def get_movers(
    index: str,
    direction: str = "up",
    change: str = "percent",
    apikey: str = None
):
    """Top 10 (up or down) movers by value or percent for a particular market.

    Args:
        index (str):     The index symbol to get movers from. Can be $COMPX, $DJI, $SPX.X (required).
        direction (str): To return movers with the specified directions of `up` or `down`. Default: `up`.
        change (str):    To return movers with the specified change types of `percent` or `value`. Default: `percent`.
        apikey (str):    API key to api.tdameritrade.com (required, can be set in env: TDA_API_KEY).

    Returns:
        response (dict): API response with price quote.
    """
    params = {
        "direction": direction,
        "change": change,
        "apikey": apikey
    }

    return _get(
        endpoint=f"https://api.tdameritrade.com/v1/marketdata/{index}/movers",
        params={ k: v for k, v in params.items() if v }
    )
