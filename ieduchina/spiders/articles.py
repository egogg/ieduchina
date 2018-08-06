# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
from selenium import webdriver

class ArticlesSpider(CrawlSpider):
	name = 'articles'
	allowed_domains = ['www.ieduchina.com', 'm.ieduchina.com']
	start_urls = [
		'http://www.ieduchina.com/home/3657.html',
		'http://www.ieduchina.com/home/3656.html',
		'http://www.ieduchina.com/home/3655.html',
		'http://www.ieduchina.com/home/3652.html'
	]

	rules = (
		Rule(LinkExtractor(allow=(), restrict_xpaths=('//*[@id="pages"]/a[last()]',)),
			callback="parse_item",
			follow=True),)

	def parse_item(self, response):
		print('[*] ' + response.url)
		item_links = response.css('.article_list_con .article_item .article_info h4 a::attr(href)').extract()
		for a in item_links:
			print('    visiting: ' + a[2:])
			print('    visiting: ' + 'm.' + a[2:])
		
	parse_start_url = parse_item