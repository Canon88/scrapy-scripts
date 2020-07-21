'''
@Author: Canon
@Date: 2020-07-11 13:41:48
@LastEditTime: 2020-07-21 17:45:06
@LastEditors: Please set LastEditors
@Description: Crawl something from Cracked.io
@FilePath: /Code/Scrapy/BBS/BBS/spiders/cracked.py
'''

import datetime
import re
import time

# -*- coding: utf-8 -*-
import scrapy

from BBS.items import BbsItem


class CrackedSpider(scrapy.Spider):
    name = 'raidforums'
    allowed_domains = ['raidforums.com']
    start_url = 'https://raidforums.com/search.php?action=do_search&keywords={}&postthread=2&author=&matchusername=1&forums%5B%5D=all&findthreadst=1&numreplies=&postdate=0&pddir=1&threadprefix%5B%5D=any&sortby=lastpost&sortordr=desc&showresults=posts&submit=Search'

    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
    }

    cookie = {}

    keywords = []   # keywords

    def start_requests(self):
        for keyword in self.keywords:
            url = self.start_url.format(keyword)
            yield scrapy.Request(url, callback=self.parse, headers=self.header, cookies=self.cookie, dont_filter=True)

    def parse(self, response):
        if response.status != 200:
            return

        raw_href = response.xpath('//table[2]//tr/td[2]/span/a[1]//@href').extract()
        href = [response.urljoin(i.strip()) for i in raw_href]

        title = response.xpath('//table[2]//tr/td[2]/span/a[1]//text()').extract()

        create_time = response.xpath('//table[2]//tr/td[7]/span//text()').extract()

        # debug
        msg = dict(zip(title, create_time))
        self.logger.debug(msg)

        check_points = self.get_nday_list(6)

        item = BbsItem()
        for i in range(len(create_time)):
            check_point = re.search('(.*) at', create_time[i]).group(1)
            if check_point in check_points:
                item['url'] = href[i]
                item['title'] = title[i]
                item['create_time'] = create_time[i]
                item['provider'] = 'Spider'
                item['producer'] = 'Raidforums'
                yield item

    def get_nday_list(self, n):
        before_n_days = []
        for i in range(0, n+1)[::-1]:
            dt = datetime.date.today() - datetime.timedelta(days=i)
            before_n_days.append(dt.strftime("%B %d, %Y"))
        return before_n_days
