'''
@Author: Canon
@Date: 2020-07-11 13:41:48
@LastEditTime: 2020-07-21 17:43:14
@LastEditors: Please set LastEditors
@Description: Crawl something from Cracked.io
@FilePath: /Code/Scrapy/BBS/BBS/spiders/cracked.py
'''

import json

# -*- coding: utf-8 -*-
import scrapy

from BBS.items import BbsItem


class CrackedSpider(scrapy.Spider):
    name = 'cracked'
    allowed_domains = ['cracked.io']
    start_url = 'https://cracked.to/search.php'

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }

    cookie = {

    }

    data = {
        'action': 'do_search',
        'keywords': 'Canon',   # Search keywords
        'postthread': '1',
        'author': '',
        'matchusername': '1',
        'forums[]': 'all',
        'findthreadst': '1',
        'numreplies': '',
        'postdate': '0',
        'pddir': '1',
        'threadprefix[]': 'any',
        'sortby': 'lastpost',
        'sortordr': 'desc',
        'showresults': 'threads',
        'submit': 'Search'
    }

    check_points = [
        'minutes',
        'hours',
        'day',
        'days'
    ]

    def start_requests(self):
        yield scrapy.FormRequest(self.start_url, callback=self.parse, headers=self.header, cookies=self.cookie, formdata=self.data, dont_filter=True)

    def parse(self, response):
        if response.status != 200:
            return

        raw_href = response.xpath('//*[contains(@id, "tid")]/@href').extract()
        href = [response.urljoin(i.strip()) for i in raw_href]

        raw_create_time = response.xpath('//*[contains(@class, "thread-date")]//text()[2]').extract()
        create_time = [i.strip() for i in raw_create_time]

        title = response.xpath('//*[contains(@id, "tid")]//text()').extract()

        msg = dict(zip(title, create_time))
        self.logger.debug(msg)

        item = BbsItem()
        for i in range(len(href)):
            check_point = create_time[i].split()[1]
            if check_point in self.check_points:
                item['url'] = href[i]
                item['title'] = title[i]
                item['create_time'] = create_time[i]
                item['provider'] = 'Spider'
                item['producer'] = 'Cracked'
                yield item
