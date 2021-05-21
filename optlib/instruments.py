from optlib.api import get_chain, get_historical

from datetime import datetime

import pandas as pd
import json


class Historical:

    def __init__(self, data):
        self.symbol = data["symbol"]
        self.empty = data["empty"]

        self.candles = []
        for c in data["candles"]:
            c["datetime"] = datetime.utcfromtimestamp(c["datetime"] / 1000)
            self.candles.append(c)

    @classmethod
    def parse(cls, resp):
        return Historical(resp)

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.parse(get_historical(*args, **kwargs))

    def to_dataframe(self):
        return pd.DataFrame([c for c in self.candles])

    def __iter__(self):
        for c in self.candles:
            yield c

class Option:

    parseDateCols = (
        "tradeTimeInLong",
        "quoteTimeInLong",
        "expirationDate",
        "lastTradingDay",
    )

    def __init__(self, data):
        self.dict = {}
        for k, v in data.items():
            if k in self.parseDateCols and v:
                v = datetime.utcfromtimestamp(v / 1000)
            self.dict.update({k: v})
            setattr(self, k, v)

    def to_dict(self):
        return self.dict

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
    def parse(cls, resp):

        if resp.get("status") != "SUCCESS":
            raise ValueError("No successful response from chain API.")

        if (strategy := resp.get("strategy")) != "SINGLE":
            raise ValueError(f"Strategy ({strategy}) is not supported. Use strategy 'SINGLE'.")

        return OptionChain(
            symbol=resp["symbol"],
            isDelayed=resp["isDelayed"],
            isIndex=resp["isIndex"],
            interestRate=resp["interestRate"],
            underlyingPrice=resp["underlyingPrice"],
            volatility=resp["volatility"],
            callExpDateMap=resp.get("callExpDateMap", dict()),
            putExpDateMap=resp.get("putExpDateMap", dict())
        )

    @classmethod
    def get(cls, *args, **kwargs):
        return cls.parse(get_chain(*args, **kwargs))

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
