from enum import Enum
from typing import Union

import numpy as np

from rumorz_data.constants import convert_entity_type_format


class ScreenerValues(Enum):
    ABS = "abs"
    CHG = "chg"


class Lookback(Enum):
    ONE_HOUR = "1H"
    SIX_HOURS = "6H"
    TWELVE_HOURS = "12H"
    ONE_DAY = "1D"
    ONE_WEEK = "7D"
    ONE_MONTH = "30D"
    THREE_MONTHS = "90D"
    ONE_YEAR = "365D"


class EntityType(Enum):
    FINANCIAL_ASSET = "financial_asset"
    COMPANY = "company"
    ORGANIZATION = "organization"
    PERSON = "person"
    PLACE = "place"


class AssetClass(Enum):
    CRYPTO = "crypto"


class SearchMethod(Enum):
    EXACT = "exact"
    CONTAINS = "contains"
    KEYWORD = "keyword"


class NodeMetrics(Enum):
    SENTIMENT = 'sentiment'
    MENTIONS = 'mentions'
    EXCITEMENT = 'excitement'
    OPTIMISM = 'optimism'
    PESSIMISM = 'pessimism'
    FEAR = 'fear'
    UNCERTAINTY = 'uncertainty'
    SURPRISE = 'surprise'


class Entity:
    def __init__(self,
                 type: Union[EntityType, str],
                 name,
                 symbol=None):
        self.type = type
        self.name = name
        if isinstance(symbol, str):
            self.symbol = symbol
        else:
            self.symbol = None


    def to_dict(self,
                format=None):
        return {
            "name": self.name,
            "type": self.type if format is None else convert_entity_type_format(getattr(self.type, 'value', self.type),
                                                                                format),
            "symbol": self.symbol
        }
