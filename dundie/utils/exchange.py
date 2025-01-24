from decimal import Decimal
from typing import Dict, List
import httpx

from dundie.settings import API_BASE_URL
from pydantic import BaseModel, Field


class USDExchangeRate(BaseModel):
    code: str = Field(default="USD")
    codein: str = Field(default="USD")
    name: str = Field(default="Dollar/Dollar")
    value: Decimal = Field(alias="high")


def get_exchange_rate(currencies: List[str]) -> Dict[str, USDExchangeRate]:
    """Get the exchange rate for a given currency."""

    def fetch_exchange_rate(currency: str) -> USDExchangeRate:
        # USD is the base currency
        if currency == "USD":
            return USDExchangeRate(high=1)
        else:
            url = API_BASE_URL.format(currency=currency)
            response = httpx.get(url, verify=False)
            if response.status_code == 200:
                data = response.json()[f"USD{currency}"]
                return USDExchangeRate(**data)
            else:
                return USDExchangeRate(high=0, name="api/error")

    return {
        currency: fetch_exchange_rate(currency)
        for currency in currencies
        if currency
    }
