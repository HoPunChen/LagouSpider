# -*- coding: utf-8 -*-
__author__ = 'HoPun'
import hashlib
import re

def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def extract_num(value):
    # 从字符串中提取出数字
    march_re = re.match(".*?(\d+).*",value)
    if march_re:
        nums = int(march_re.group(1))
    else:
        nums = 0
    return nums