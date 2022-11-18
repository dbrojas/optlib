from optlib import api

from datetime import datetime

import pandas as pd
import json


class Pricehistory:

    def __init__(
        self,
        symbol: str,
        empty: str,
        candles: list
    ):
        self.symbol = empty
        self.empty = empty

        self.candles = []
        for c in candles:
            c["datetime"] = datetime.utcfromtimestamp(c["datetime"] / 1000)
            self.candles.append(c)

    def __iter__(self):
        for c in self.candles:
            yield c

    @classmethod
    def parse_tda_response(
        cls,
        response: dict
    ):
        return cls(
            symbol=response["symbol"],
            empty=response["empty"],
            candles=response["candles"]
        )

    @classmethod
    def get(
        cls,
        symbol: str,
        period_type: str = "year",
        period: int = 1,
        frequency_type: str = "daily",
        frequency: int = 1,
        start_date: datetime = None,
        end_date: datetime = None,
        need_extended_hours_data: bool = False,
        apikey: str = None
    ):
        response = api.get_pricehistory(
            symbol=symbol,
            period_type=period_type,
            period=period,
            frequency_type=frequency_type,
            frequency=frequency,
            start_date=start_date,
            end_date=end_date,
            need_extended_hours_data=need_extended_hours_data,
            apikey=apikey
        )
        return cls.parse_tda_response(response)

    def to_dataframe(self):
        return pd.DataFrame(self)

class Option:

    parse_date_cols = (
        "tradeTimeInLong",
        "quoteTimeInLong",
        "expirationDate",
        "lastTradingDay",
    )

    def __init__(self, data):
        for k, v in data.items():
            if k in self.parse_date_cols and v:
                v = datetime.utcfromtimestamp(v / 1000)
            setattr(self, k, v)

    def to_dict(self):
        return self.__dict__

class OptionChain:

    def __init__(
        self,
        symbol,
        isDelayed,
        isIndex,
        interestRate,
        underlyingPrice,
        volatility,
        callExpDateMap,
        putExpDateMap
    ):
        self.symbol = symbol
        self.isDelayed = isDelayed
        self.isIndex = isIndex
        self.interestRate = interestRate
        self.underlyingPrice = underlyingPrice
        self.volatility = volatility
        self.expDateMap = tuple(callExpDateMap.items()) + tuple(putExpDateMap.items())

    @classmethod
    def parse_tda_response(
        cls,
        response
    ):

        if response.get("status") != "SUCCESS":
            raise ValueError("No successful response from chain API.")

        if (strategy := response.get("strategy")) != "SINGLE":
            raise ValueError(f"Strategy ({strategy}) is not supported. Use strategy 'SINGLE'.")

        return OptionChain(
            symbol=response["symbol"],
            isDelayed=response["isDelayed"],
            isIndex=response["isIndex"],
            interestRate=response["interestRate"],
            underlyingPrice=response["underlyingPrice"],
            volatility=response["volatility"],
            callExpDateMap=response.get("callExpDateMap", {}),
            putExpDateMap=response.get("putExpDateMap", {})
        )

    @classmethod
    def get(cls,
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
        option_type: str = "all",
        apikey: str = None
    ):
        response = api.get_chain(
            symbol=symbol,
            contract_type=contract_type,
            strike_count=strike_count,
            include_quotes=include_quotes,
            strategy=strategy,
            interval=interval,
            strike=strike,
            range=range,
            from_date=from_date,
            to_date=to_date,
            volatility=volatility,
            underlying_price=underlying_price,
            interest_rate=interest_rate,
            days_to_expiration=days_to_expiration,
            exp_month=exp_month,
            option_type=option_type,
            apikey=apikey
        )
        return cls.parse_tda_response(response)

    @classmethod
    def from_json(cls, filepath):

        with open(filepath, "r") as f:
            resp = json.load(f)

        return cls.parse(resp)

    @property
    def options(self):
        return list(self)

    @property
    def expiration_dates(self):
        return list({opt.expirationDate for opt in self.options})

    def to_dataframe(self):
        return pd.DataFrame([opt.to_dict() for opt in self.options])

    def __iter__(self):
        for _, strikes in self.expDateMap:
            for _, data in strikes.items():
                for r in data:
                    yield Option(r)
