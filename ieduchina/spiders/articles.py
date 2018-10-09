# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
# from selenium import webdriver
from time import sleep
import datetime
import time

class ArticlesSpider(scrapy.Spider):
	name = 'articles'
	allowed_domains = ['www.ieduchina.com', 'm.ieduchina.com']
	user_ids = [3652, 3655, 3656, 3657]
	request_url = 'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles'
	pc_counter_url = 'www.ieduchina.com/api.php?'
	m_counter_url = 'm.ieduchina.com/api.php?'

	url_pattern = re.compile(r'^\/\/(.*)(m\.ieduchina\.com)(.*)')
	article_id_parttern = re.compile(r'^\/\/.*\/([0-9]+).html$')

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
			user_id = response.meta['user_id']
			page = response.meta['page']
			print('[*] visiting user_id: ' +  str(user_id) + ' page : ' + str(page))

			item_links = response.css('div.collect-item h3.title a::attr(href)').extract()
			for a in item_links:
				m = self.url_pattern.search(a)
				if m :
					url_prefix = m.group(1)
					url_base = m.group(3)
					try:
						pc_link = url_prefix + 'ieduchina.com' + url_base
						print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '] pc: ' + pc_link)
						# self.browser.get(pc_link)
					except:
						pass
					# sleep(self.interval)

					try:
						m_link = url_prefix + 'm.ieduchina.com' + url_base
						print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']  m: ' + m_link)
						# self.browser.get(m_link)
					except:
						pass
					# sleep(self.interval)

				id_m = self.article_id_parttern.search(a)
				if id_m :
					article_id = id_m.group(1)
					print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']  article id: '+ article_id)
					counter_params = 'op=count&id=' + article_id + '&modelid=1'
					pc_request_url = self.pc_counter_url + counter_params
					m_request_url = self.m_counter_url + counter_params
					print(pc_counter_url)
					print(m_counter_url)

			formdata = {
				'page': str(page + 1),
				'userid': str(user_id)
			}
			yield scrapy.FormRequest(url=self.request_url, method='POST', formdata=formdata, callback=self.parse, meta={'user_id': user_id, 'page' : page + 1})
		else:
			return
	