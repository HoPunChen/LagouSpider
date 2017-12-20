# -*- coding: utf-8 -*-
__author__ = 'HoPun'

import re

def extract_num(value):
    # 从字符串中提取出数字
    march_re = re.match(".*?(\d+).*",value)
    if march_re:
        nums = int(march_re.group(1))
    else:
        nums = 0
    return nums