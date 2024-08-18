import datetime

import requests
from requests import RequestException

from .constants import API_URL, DEFAULT_TIMEOUT
from .exception import CbrfRatesError
from .utils import convert_date_to_string, parse_xml_response


class CbrfRatesClient:
    def __init__(self, timeout: float | tuple[float, float] | tuple[float, None] | None = DEFAULT_TIMEOUT):
        self.timeout = timeout
        self.headers = {"accept": "application/json"}

    def get_rates(self, date: datetime.date = None) -> list[dict]:
        url = API_URL
        if date:
            date_str = convert_date_to_string(date)
            url += f"?date_req={date_str}"

        try:
            response = requests.get(
                url=url,
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
        except RequestException as err:
            raise CbrfRatesError("Request error: ", err) from err

        return parse_xml_response(response)
