import time

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
r = requests.get(url="https://www.copart.com/public/data/lotdetails/solr/46216602", verify=False,  # noqa
                 headers=headers, )  # noqa

# print(r.json())
print(int(round(time.time() * 1000)))
# LU -> Last Update Time in ms
# ad -> Action start date
