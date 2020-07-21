'''
@Author: Canon
@Date: 2020-07-11 13:41:06
@LastEditTime: 2020-07-21 17:50:13
@LastEditors: Please set LastEditors
@Description: Blog Spider
@FilePath: /Code/Scrapy/BBS/BBS/pipelines.py
'''
# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


from slack_webhook import Slack


class BbsPipeline(object):
    def process_item(self, item, spider):
        return item


class SlackPipeline(object):
    def __init__(self, webhook, cache_db):
        self.webhook = webhook
        self.cache_db = cache_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            webhook=crawler.settings.get('WEBHOOK'),
            cache_db=crawler.settings.get('CACHE_DB')
        )

    def open_spider(self, spider):
        self.slack = Slack(url=self.webhook)

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):

        # local cache.db clean duplicate
        with open(self.cache_db) as f:
            cache = [line.strip() for line in f]
        if item['url'] in cache:
            return item
        with open(self.cache_db, 'a') as f:
            f.write(item['url'] + '\n')

        # Slack msg
        msg = "禀大王，前方探子来报！"
        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*禀大王，前方探子来报：*"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Title:    {}*".format(item['title'])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Creation time:    {}*".format(item['create_time'])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Producer:    {}*".format(item['producer'])
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "<{}|*传送门*>".format(item['url'])
                }
            },
            {
                "type": "divider"
            }
        ]

        self.slack.post(text=msg, blocks=blocks)
        return item
