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

	opts = webdriver.FirefoxOptions()
	opts.add_argument("--headless")
	browser = webdriver.Firefox(firefox_options = opts)

	def parse_item(self, response):
		print('[*] ' + response.url)
		interval = int(getattr(self, 'interval', '30'))
		repeat = int(getattr(self, 'repeat', '1'))
		repeat_interval = int(getattr(self, 'rinterval', '5'))
		item_links = response.css('.article_list_con .article_item .article_info h4 a::attr(href)').extract()
		for a in item_links:
			try:
				pc_link = 'http://' + a[2:]
				for i in xrange(1, repeat):
					print('    visiting(' + i + '): ' + pc_link)
					self.browser.get(pc_link)
					sleep(repeat_interval)
				sleep(interval)

				m_link = 'http://m.' + a[2:]
				for i in xrange(1, repeat):
					print('    visiting(' + i + '): ' + m_link)
					self.browser.get(m_link)
					sleep(repeat_interval)
				sleep(interval)
			except Exception as e:
				pass
		
	parse_start_url = parse_item