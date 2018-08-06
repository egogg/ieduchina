# -*- coding: utf-8 -*-
import scrapy


class ArticlesSpider(scrapy.Spider):
    name = 'articles'
    allowed_domains = ['ieduchina.com']
    start_urls = ['http://ieduchina.com/']

    def parse(self, response):
        pass
