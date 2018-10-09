# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
# from selenium import webdriver
from time import sleep

class ArticlesSpider(scrapy.Spider):
	name = 'articles'
	allowed_domains = ['www.ieduchina.com', 'm.ieduchina.com']
	user_ids = [3652, 3655, 3656, 3657]
	request_url = 'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles'
	# start_urls = [
	# 	'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles&userid=3652',
	# 	'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles&userid=3655',
	# 	'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles&userid=3656',
	# 	'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles&userid=3657'
	# ]
	# start_urls = [
	# 	'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles&userid=3652'
	# ]

	# rules = (
	# 	Rule(LinkExtractor(allow=(), restrict_xpaths=('//div[@class="collect-item"]',)),
	# 		callback="parse_item",
	# 		follow=True),)

	url_pattern = re.compile(r'^(\/\/www\.|\/\/)(.*)')

	# opts = webdriver.FirefoxOptions()
	# opts.add_argument("--headless")
	# browser = webdriver.Firefox(firefox_options = opts)

	def __init__(self, interval = '30', repeat = '1', timeout = '10', *args, **kwargs):
		super(ArticlesSpider, self).__init__(*args, **kwargs)
		self.interval = int(interval)
		self.repeat = int(repeat)
		self.timeout = int(timeout)

		# self.start_urls = self.start_urls * self.repeat
		# self.browser.set_page_load_timeout(self.timeout)

	def start_requests(self):
		for user_id in self.user_ids :
			formdata = {
				'page': '1',
				'userid': str(user_id)
			}
			yield scrapy.FormRequest(url=self.request_url, method='POST', formdata=formdata, callback=self.parse, meta={'user_id': user_id, 'page' : 1})

	def parse(self, response):
		if response.xpath('//div[@class="collect-item"]'):
			item_links = response.css('div.collect-item h3.title a::attr(href)').extract()
			print(item_links)

			print('user_id: ' +  str(response.meta['user_id']) + ' page : ' + str(response.meta['page']))
			formdata = {
				'page': str(response.meta['page'] + 1),
				'userid': str(response.meta['user_id'])
			}
			yield scrapy.FormRequest(url=self.request_url, method='POST', formdata=formdata, callback=self.parse)
		else:
			return
		# for a in item_links:
		# 	m = self.url_pattern.search(a)
		# 	if m :
		# 		url_base = m.group(2)
		# 		try:
		# 			pc_link = 'http://' + url_base
		# 			print('    visiting: ' + pc_link)
		# 			self.browser.get(pc_link)
		# 		except:
		# 			pass
		# 		sleep(self.interval)

		# 		try:
		# 			m_link = 'http://m.' + url_base
		# 			print('    visiting: ' + m_link)
		# 			self.browser.get(m_link)
		# 		except:
		# 			pass
		# 		sleep(self.interval)
	