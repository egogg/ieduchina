# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
import os
from selenium import webdriver
from time import sleep

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

	browser = webdriver.Firefox()

	def parse_item(self, response):
		print('[*] ' + response.url)
		interval = int(getattr(self, 'interval', '30'))
		item_links = response.css('.article_list_con .article_item .article_info h4 a::attr(href)').extract()
		for a in item_links:
			pc_link = a[2:]
			print('    visiting: ' + pc_link)
			self.browser.get(pc_link)
			sleep(interval)

			m_link = 'm.' + a[2:]
			print('    visiting: ' + m_link)
			self.browser.get(m_link)
			sleep(interval)
		
	parse_start_url = parse_item