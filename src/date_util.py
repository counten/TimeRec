# -*- coding:utf-8 -*-
"""
Created on 8/20/2018
Author: wbq813 (wbq813@foxmail.com)
"""
import time

from src.base_date_util import CommonDateUtil


class DateUtil(CommonDateUtil):
    # python 的时间戳时10位，也就是秒，1534901899.2290354
    def __init__(self, t=time.time()):
        self._time = t

    def __copy__(self):
        new_date_util = DateUtil()
        new_date_util._time = self._time
        return new_date_util

    def change_year(self, year):
        self._time += year * self.ONE_YEAR_SECOND

    def change_month(self, month):
        self._time += month * self.ONE_MONTH_SECOND

    def change_day(self, day):
        self._time += day * self.ONE_DAY_SECOND

    def change_hour(self, hour):
        self._time += hour * self.ONE_HOUR_SECOND

    def change_minute(self, minute):
        self._time += minute * self.ONE_MINUTE_SECOND

    def change_second(self, second):
        self._time += second

    def change_week(self, week, day=1):
        # 回到某个周一
        interval = -time.localtime().tm_wday + 7 * week
        self.change_day(interval)
        # 定位周几
        day2 = day - 1
        if 6 >= day2 >= 1:
            self.change_day(day2)

    def get_timestamp(self):
        return self._time

    def get_time(self):
        return time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(self._time))

    def get_time_list(self):
        local_time = time.localtime(self._time)
        res = list()
        res.append(local_time.tm_year)
        res.append(local_time.tm_mon)
        res.append(local_time.tm_mday)
        res.append(local_time.tm_hour)
        res.append(local_time.tm_min)
        res.append(local_time.tm_sec)
        return res


if __name__ == '__main__':
    date = DateUtil(time.time())
    date.change_week(1, 6)
    print(date.get_time())
