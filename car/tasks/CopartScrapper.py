import asyncio
import datetime
from functools import reduce
from pprint import pprint

import aiohttp
import requests
from aiohttp import ClientResponseError

headers = {
    "Host": "www.copart.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
}


def check_rd(run_and_drives: str):
    if run_and_drives is not None and run_and_drives.upper() == "RUNS AND DRIVES":
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
                     verify=True,
                     headers=headers)
    print(r.status_code)
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

    return car


def get_loot_ids() -> list:
    # copart_cars = CopartCar.objects.all()
    # return [car.loot_id for car in copart_cars]
    a = [47550752, 51941871, 35144082, 33229472, 41334322, 47285422, 46912882, 50159332, 54496121, 50246012]
    return a


def retry_get(response):
    counter = 0
    if "Incapsula" in str(response) and counter > 4:
        counter += 1
        retry_get(response)
    return response


def mi_to_km(miles):
    if isinstance(miles, (int, str, float)) and miles is not None:
        return int(miles * 1.609344)
    return None


async def async_get_car_data(session: aiohttp.ClientSession, loot_id):
    counter = 0
    url = f"https://www.copart.com/public/data/lotdetails/solr/{loot_id}"

    try:
        async with session.get(url, headers=headers) as response:
            car = await response.json(encoding="UTF-8")
            if "Incapsula" in car and counter > 4:
                counter += 1
                print("failed to scrap data ", counter)
                await async_get_car_data(session, loot_id)
            if response.status == 200 and deep_get(car, 'data.lotDetails'):

                car = {"START": "+++++++++++++++++++++++++++++++++",
                       'VIN': deep_get(car, 'data.lotDetails.fv'),  # fv
                       'loot_id': loot_id,  # loot_id
                       'last_update': ms_to_date(deep_get(car, 'data.lotDetails.lu')),  # lu
                       'auction_date': ms_to_date(deep_get(car, 'data.lotDetails.ad')),  # ad
                       'odometer_mi': deep_get(car, 'data.lotDetails.orr'),  # orr
                       'odometer_km': mi_to_km(deep_get(car, 'data.lotDetails.orr')),  # orr
                       'r&d': check_rd(deep_get(car, 'data.lotDetails.lcd')),  # lcd
                       'make': deep_get(car, 'data.lotDetails.lmg'),  # lmg
                       'model': deep_get(car, 'data.lotDetails.lm'),  # lm
                       'year': deep_get(car, 'data.lotDetails.lcy'),  # lcy
                       'currentBid': deep_get(car, 'data.lotDetails.dynamicLotDetails.currentBid'),  # currentBid
                       }
                pprint(car)
            else:
                print("There is no car with this ID")
    except ClientResponseError as e:
        print("Can't scrap data for loot id: ", loot_id)


async def copart_scrapper(loop):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for loot_id in get_loot_ids():
            tasks.append(loop.create_task(async_get_car_data(session, loot_id)))
        await asyncio.wait(tasks)


def run_async_scrapper():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(copart_scrapper(loop))
