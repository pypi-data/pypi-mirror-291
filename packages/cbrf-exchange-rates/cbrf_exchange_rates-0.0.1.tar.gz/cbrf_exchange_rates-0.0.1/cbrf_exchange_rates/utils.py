from datetime import datetime
from decimal import Decimal, InvalidOperation
from xml.etree import ElementTree

from requests import Response

from .constants import DATE_FORMAT
from .exception import ConvertError


def convert_date_to_string(date: datetime.date) -> str:
    try:
        return date.strftime(DATE_FORMAT)
    except ValueError as err:
        raise ConvertError("Convert error to str: ", err) from err


def convert_to_decimal(value: str) -> Decimal:
    try:
        return Decimal(value.replace(',', '.'))
    except InvalidOperation as err:
        raise ConvertError("Convert error to decimal: ", err) from err


def parse_xml_response(response: Response) -> list[dict]:
    result = []
    root = ElementTree.fromstring(response.content)

    for value in root.findall('Valute'):
        result.append(
            {
                "id": value.find('NumCode').text,
                "code": value.find('CharCode').text,
                "name": value.find('Name').text,
                "rate": convert_to_decimal(value.find('Value').text),
            }
        )
    return result
