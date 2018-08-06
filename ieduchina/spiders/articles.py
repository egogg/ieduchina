# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
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

	url_pattern = re.compile(r'^(\/\/www\.|\/\/)(.*)')

	opts = webdriver.FirefoxOptions()
	opts.add_argument("--headless")
	browser = webdriver.Firefox(firefox_options = opts)

	def __init__(self, interval = '30', repeat = '1', *args, **kwargs):
		super(ArticlesSpider, self).__init__(*args, **kwargs)
		self.interval = int(interval)
		self.repeat = int(repeat)
		self.start_urls = self.start_urls * self.repeat

	def parse_item(self, response):
		print('[*] ' + response.url)
		item_links = response.css('.article_list_con .article_item .article_info h4 a::attr(href)').extract()
		for a in item_links:
			m = self.url_pattern.search(a)
			if m :
				url_base = m.group(2)
				try:
					pc_link = 'http://' + url_base
					print('    visiting: ' + pc_link)
					# self.browser.get(pc_link)
					sleep(self.interval)

					m_link = 'http://m.' + url_base
					print('    visiting: ' + m_link)
					# self.browser.get(m_link)
					sleep(self.interval)
				except Exception as e:
					pass
		
	parse_start_url = parse_item