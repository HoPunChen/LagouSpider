# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose
from w3lib.html import remove_tags
from utils.common import extract_num

class LagouspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

def replace_splash(value):
    return value.replace("/","")

def handle_strip(value):
    return value.strip()

def handle_jobaddr(value):
    addr_list = value.split("\n")
    addr_list = [item.strip() for item in addr_list if item.strip() != "查看地图"]
    return "".join(addr_list)

class LagouJobItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()

class LagouJobItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field(
        input_processor = MapCompose(replace_splash),
    )
    work_years = scrapy.Field(
        input_processor = MapCompose(replace_splash),
    )
    degree_need = scrapy.Field(
        input_processor = MapCompose(replace_splash),
    )
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field(
        input_processor = MapCompose(handle_strip)
    )
    job_addr = scrapy.Field(
        input_processor = MapCompose(remove_tags,handle_jobaddr)
    )
    company_name = scrapy.Field(
        input_processor = MapCompose(handle_strip)
    )

    company_url = scrapy.Field()
    crawl_time = scrapy.Field()
    crawl_update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
             insert into lagou_job(title, url, salary, job_city, work_years, degree_need,
            job_type, publish_time, job_advantage, job_desc, job_addr, company_name, company_url, job_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE job_desc=VALUES(job_desc)
        """

        job_id = extract_num(self["url"])
        params = (self["title"],self["url"],self["salary"],self["job_city"],self["work_years"],self["degree_need"],
                  self["job_type"],self["publish_time"],self["job_advantage"],self["job_desc"],self["job_addr"],
                  self["company_name"],self["company_url"],job_id)

        return insert_sql,params

