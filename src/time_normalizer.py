# -*- coding:utf-8 -*-
"""
Created on 8/20/2018
Author: wbq813 (wbq813@foxmail.com)
"""
import codecs
import re
import time

from src.date_util import DateUtil
from src.string_pre_process import StrPreProcess
from src.time_unit import TimeUnit


class TimeNormalizer:
    serial_version_UID = 463541045644656392
    time_base = None
    old_time_base = None
    patterns = None
    target = None
    time_token = list()
    is_prefer_future = True
    file_path = "time_re"

    def __init__(self, prefer_future=True):
        # 是否关闭未来倾向
        self.is_prefer_future = prefer_future
        if self.patterns is None:
            self.read()

    def read(self):
        f = codecs.open(self.file_path, 'r', 'utf-8')
        str_in = f.read()
        self.patterns = re.compile(str_in)

    def pre_process(self):
        str_target = self.target
        # 清理空白字符
        str_target = StrPreProcess.del_keyword(str_target, r"\\s+")
        # 清理语气助词
        str_target = StrPreProcess.del_keyword(str_target, "[的]+")
        # 大写数字转换
        str_target = StrPreProcess.num_translate(str_target)
        # TODO 处理大小写标点符号
        self.target = str_target

    def time_ex(self):
        str_target = self.target
        it = re.finditer(self.patterns, str_target)
        start = -1
        end = -1
        match_count = 0
        str_map_arr = dict()
        for m in it:
            start = m.start()
            if end == start:
                match_count -= 1
                str_map_arr[match_count] = str_map_arr[match_count] + m.group()
            else:
                str_map_arr[match_count] = m.group()
            end = m.end()
            match_count += 1

        # 时间上下文： 前一个识别出来的时间会是下一个时间的上下文，
        # 用于处理：周六3点到5点这样的多个时间的识别，第二个5点应识别到是周六的。
        for i in range(match_count):
            clean_record = False
            if i == 0:
                clean_record = True
            time_unit = TimeUnit(str_map_arr[i], self.time_base, self.old_time_base, clean_record)
            if time_unit.time != -28800000:
                self.time_token.append(time_unit)

    def parse(self, str_target):
        # 清除上次存储的结果
        if len(self.time_token) > 0:
            self.time_token.clear()
        self.target = str_target
        self.time_base = DateUtil(time.time())
        self.old_time_base = self.time_base

        self.pre_process()
        self.time_ex()
        return self.time_token


if __name__ == '__main__':
    tn = TimeNormalizer()
    test_list = ["薛之谦两年前的演唱会",
                 "薛之谦两周前的演唱会",
                 "我想听邓丽君八十年代到九十年代的安静的歌",
                 "我想听周杰伦去年的歌",
                 "我想听王菲上个月的歌",
                 "昨天的表演",
                 "下午三点开会",
                 "明天上午8点到下午3点",
                 "三天前"]
    for query in test_list:
        res = tn.parse(query)
        for r in res:
            print(r.time_expression, r.time_norm, r.time)
        print("----------------------")
    print(tn.time_token)
