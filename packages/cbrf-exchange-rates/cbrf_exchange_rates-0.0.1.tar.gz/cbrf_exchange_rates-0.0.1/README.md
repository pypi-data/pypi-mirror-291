## Python client for CBRF Rates API
cbrf_exchange_rates - это модуль для скачивания курсов валют с сайта cbr.ru (Центральный банк Российской Федерации)

Модуль использует открытое [API](https://cbr.ru/development/sxml/).

Лицензия MIT.

## Зависимости
* python==3.12
* requests==2.32.3

## Установка
```
pip install cbrf_exchange_rates
```

## Использование
```python
from cbrf_exchange_rates.service import CbrfRatesClient

cbrf_client = CbrfRatesClient()
cbrf_client.get_rates()
```

Результат:
```
[
    {
        'code': 'AUD',
        'id': '036',
        'name': 'Австралийский доллар',
        'rate': Decimal('58.9448')
     },
     {
         'code': 'AZN',
         'id': '944',
         'name': 'Азербайджанский манат',
         'rate': Decimal('52.2978')
     }
]
```

