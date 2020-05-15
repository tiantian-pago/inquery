# coding = utf-8

"""
获取车站名称和编号
"""

import re
import requests
import pprint

url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9109'
response = requests.get(url, verify=False)
station = re.findall(u'([\u4e00-\u9fa5]+)\|([A-Z]+)', response.text)
#pprint(station, indent=4)
#pprint(dict(station), indent=4))
stations = "station = " + pprint.pformat(dict(station))
print(stations)
with open("station.py", "w") as f:
    f.write(stations)