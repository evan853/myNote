#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-04-13 16:42:12
# Project: taobaomm

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
    }
    
    def __init__(self):
        self.page_num=1
        self.total_num=30
        self.base_url='https://mm.taobao.com/json/request_top_list.htm?page='

    @every(minutes=24 * 60)
    def on_start(self):
        while self.page_num<=self.total_num:
            url=self.base_url+str(self.page_num)
            print url
            self.crawl(url, callback=self.index_page)
            self.page_num+=1

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('a[href^="http"]').items():
            self.crawl(each.attr.href, callback=self.detail_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "title": response.doc('title').text(),
        }
