# -*- coding=utf-8 -*-
"""命令行火车票查看器
Usage:
    tickets [-gdtkz] <from> <to> <date>

Options:
    -h,--help   显示帮助菜单
    -g          高铁
    -d          动车
    -t          特快
    -k          快速
    -z          直达

Examples:
    tickets 苏州 南京 2016-10-10
    tickets -dg 成都 南京 2016-10-10
"""
import requests
from docopt import docopt
from station import station
from prettytable import PrettyTable
from colorama import init, Fore

init()

class TrainsCollection:
    header = '车次 车站 时间 历时 商务座 一等 二等 高级软卧 软卧 动卧 硬卧 软座 硬座 无座'.split()

    def __init__(self, available_trains, options):
        """查询到的火车班次集合

        :param available_trains: 一个列表，包含可读的火车班次，每个
                                火车班次是一个字典
        :param options: 查询的选项，如高铁，动车，etc...
        """
        self.available_trains = available_trains
        self.options = options

    def __get__duration(self, raw_train):
        duration = raw_train[9].replace(':', '小时') + '分'
        if duration.startswith('00'):
            return duration[4:]
        elif duration.startswith('0'):
            return duration[1:]
        else:
            return duration

    @property
    def trains(self):
        station_new = dict(zip(station.values(), station.keys()))
        for raw_trains in self.available_trains:
            raw_train = raw_trains.split('|')[1:]
            train_no = raw_train[2]
            initial = train_no[0].lower()
            if not self.options or initial in self.options:
                train_no = train_no                                                        # 车次
                stations = '\n'.join([Fore.GREEN + station_new.get(raw_train[5]) + Fore.RESET,
                               Fore.RED + station_new.get(raw_train[6]) + Fore.RESET])         # 车站
                dates = '\n'.join([Fore.GREEN + raw_train[7] + Fore.RESET,
                              Fore.RED + raw_train[8] + Fore.RESET])                       # 时间
                range_time = self.__get__duration(raw_train)                               # 历时
                sw_num = raw_train[-7] or '--'                                             # 商务座
                yd_num = raw_train[-8] or '--'                                             # 一等座
                ed_num = raw_train[-9] or '--'                                             # 二等座
                gj_num = raw_train[-18] or '--'                                            # 高级软卧
                rw_num = raw_train[-16] or '--'                                            # 软卧
                dw_num = raw_train[26] or '--'                                             # 动卧
                yw_num = raw_train[-11] or '--'                                            # 硬卧
                rz_num = raw_train[23] or '--'                                             # 软座
                yz_num = raw_train[-10] or '--'                                             # 硬座
                wz_num = raw_train[-13] or '--'                                            # 无座

                data = {
                    'train_no': train_no,
                    'stations':  stations,
                    'dates': dates,
                    'range_time': range_time,
                    'sw_num': sw_num,
                    'yd_num': yd_num,
                    'ed_num': ed_num,
                    'gj_num': gj_num,
                   'rw_num': rw_num,
                   'dw_num': dw_num,
                   'yw_num': yw_num,
                   'rz_num': rz_num,
                   'yz_num': yz_num,
                   'wz_num': wz_num
                }

            yield data.values()

    def pretty_print(self):
        pt = PrettyTable()
        pt.field_names = self.header
        for train in self.trains:
            pt.add_row(train)
        print(pt)

def cli():
    """command-line interface"""
    arguments = docopt(__doc__)
    from_station = station.get(arguments['<from>'])
    to_station = station.get(arguments['<to>'])
    date = arguments['<date>']
    url= ('https://kyfw.12306.cn/otn/leftTicket/queryT?'
          'leftTicketDTO.train_date={}&leftTicketDTO.from_station={}'
          '&leftTicketDTO.to_station={}&purpose_codes=ADULT').format(date, from_station, to_station)
    options = [
        key for key, value in arguments.items() if value is True
    ]
    requests.packages.urllib3.disable_warnings()
    response = requests.get(url, verify=False)   # 添加verify=False参数不验证证书
    if response.status_code == 200:
        try:
            available_trains = response.json()['data']['result']
            TrainsCollection(available_trains, options).pretty_print()
        except:
            print('请求错误，数据获取失败')
    else:
        print('获取火车数据失败')

if __name__ == '__main__':
    cli()