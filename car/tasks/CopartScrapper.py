import datetime
from functools import reduce
from pprint import pprint

import requests

headers = {
    "Host": "www.copart.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}


def check_rd(run_and_drives: str):
    if run_and_drives.upper() == "RUNS AND DRIVES":
        return True
    return False


def deep_get(dictionary, keys, default=None):
    return reduce(lambda d, key: d.get(key, default) if isinstance(d, dict) else default, keys.split("."), dictionary)


def ms_to_date(ms):
    if ms:
        return datetime.datetime.fromtimestamp(ms / 1000.0)
    return None


def read_car_data(lot_id: int) -> dict:
    r = requests.get(url=f"https://www.copart.com/public/data/lotdetails/solr/{lot_id}",  # noqa
                     verify=False,
                     headers=headers)
    car: dict = r.json()
    car = {'VIN': deep_get(car, 'data.lotDetails.fv'),  # fv
           'last_update': ms_to_date(deep_get(car, 'data.lotDetails.lu')),  # lu
           'auction_date': ms_to_date(deep_get(car, 'data.lotDetails.ad')),  # ad
           'odometer_mi': deep_get(car, 'data.lotDetails.orr'),  # orr
           'odometer_km': int(deep_get(car, 'data.lotDetails.orr') * 1.609344),  # orr
           'r&d': check_rd(deep_get(car, 'data.lotDetails.lcd')),  # lcd
           'make': deep_get(car, 'data.lotDetails.lmg'),  # lmg
           'model': deep_get(car, 'data.lotDetails.lm'),  # lm
           'year': deep_get(car, 'data.lotDetails.lcy'),  # lcy
           'currentBid': deep_get(car, 'data.lotDetails.dynamicLotDetails.currentBid'),  # currentBid
           }
    pprint(car)

    return car
