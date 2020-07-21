'''
@Author: Canon
@Date: 2020-07-11 13:41:06
@LastEditTime: 2020-07-21 17:45:35
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /Code/Scrapy/BBS/BBS/items.py
'''
# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BbsItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    create_time = scrapy.Field()
    modify_time = scrapy.Field()
    producer = scrapy.Field()
    provider = scrapy.Field()