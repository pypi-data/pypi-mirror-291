import time
import requests
import xmltodict
from enum import StrEnum
from datetime import datetime, timedelta
from functools import lru_cache, wraps


class Currency(StrEnum):
    RON = "RON"
    AED = "AED"
    AUD = "AUD"
    BGN = "BGN"
    BRL = "BRL"
    CAD = "CAD"
    CHF = "CHF"
    CNY = "CNY"
    CZK = "CZK"
    DKK = "DKK"
    EGP = "EGP"
    EUR = "EUR"
    GBP = "GBP"
    HUF = "HUF"
    INR = "INR"
    JPY = "JPY"
    KRW = "KRW"
    MDL = "MDL"
    MXN = "MXN"
    NOK = "NOK"
    NZD = "NZD"
    PLN = "PLN"
    RSD = "RSD"
    RUB = "RUB"
    SEK = "SEK"
    THB = "THB"
    TRY = "TRY"
    UAH = "UAH"
    USD = "USD"
    XAU = "XAU"
    XDR = "XDR"
    ZAR = "ZAR"

    @classmethod
    def values(cls):
        return {e.value for e in cls}


def ttl_lru_cache(seconds: int, maxsize: int | None = None):
    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        func.lifetime = seconds
        func.expiration = time.time() + func.lifetime

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if time.time() >= func.expiration:
                func.cache_clear()
                func.expiration = time.time() + func.lifetime
            return func(*args, **kwargs)

        wrapped_func.cache_info = func.cache_info
        wrapped_func.cache_clear = func.cache_clear
        return wrapped_func

    return wrapper_cache


def format_date(date: str = None):
    """
    Convert string date in '2024-07-31' (YYYY-MM-DD) format.
    If date is in the future, the latest date will be returned.
    """

    previous_date = datetime.now().date() - timedelta(days=1)
    date_obj = (
        previous_date if date is None else datetime.strptime(date, "%Y-%m-%d").date()
    )

    if date_obj > previous_date:
        date_obj = previous_date

    return date_obj


@ttl_lru_cache(seconds=24*60*60) # 24 hours
def get_exchange_rates_for_year(year: int = None):
    """
    Make a request to BNR API to get the XML with rates for the year provided.
    If year is not provided will get the latest rates for current date.

    The return will be a dictionary like:

    {'2024-01-03': {'AED': 1.239,
          'AUD': 3.0693,
          'CAD': 3.4127,
          etc},
      'YYYY-MM-DD': {'CURRENCY': RON_VALUE}
    }

    https://www.bnr.ro/nbrfxrates.xml
    https://www.bnr.ro/nbrfxrates10days.xml
    https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml
    """

    if year > datetime.now().date().year:
        raise ValueError("Can't get BNR rates from the future.")

    bnr_xml_url = (
        "https://www.bnr.ro/nbrfxrates.xml"
        if year is None
        else f"https://www.bnr.ro/files/xml/years/nbrfxrates{year}.xml"
    )

    r = requests.get(bnr_xml_url)
    r.raise_for_status()

    bnr_ron_rates = xmltodict.parse(r.content)

    exchange_rates = {}
    for entries in bnr_ron_rates["DataSet"]["Body"]["Cube"]:
        rates = {}
        for entry in entries["Rate"]:
            rates[entry["@currency"]] = round(
                float(entry["#text"]) * int(entry.get("@multiplier", 1)), 4
            )
        exchange_rates[entries["@date"]] = rates

    return exchange_rates


def ron_exchange_rate(ammount: float, currency: Currency, date: str = None):
    """
    currency: one of Currency StrEnum value
    date: string isoformat date like '2024-07-31' (YYYY-MM-DD)

    Usage:

    ron_to_eur = ron_exchange_rate(
        ammount=1, currency=Currency.EUR
    )

    """

    if currency == Currency.RON:
        return ammount

    date_obj = format_date(date)

    exchange_rates = get_exchange_rates_for_year(date_obj.year)

    if date_obj.isoformat() not in exchange_rates:
        date_obj = max(
            [
                datetime.strptime(date, "%Y-%m-%d").date()
                for date in exchange_rates.keys()
            ]
        )

    day_rates = exchange_rates[date_obj.isoformat()]

    return round(ammount * day_rates[currency], 2)
