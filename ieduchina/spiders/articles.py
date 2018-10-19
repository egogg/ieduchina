# -*- coding: utf-8 -*-
import scrapy


import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re
from time import sleep
import datetime
import time

class ArticlesSpider(scrapy.Spider):
	name = 'articles'
	allowed_domains = ['www.ieduchina.com', 'm.ieduchina.com']
	user_ids = [3652, 3655, 3656, 3657]
	request_url = 'http://m.ieduchina.com/index.php?m=user&c=home&a=loadarticles'
	pc_counter_url = 'https://www.ieduchina.com/api.php?'
	m_counter_url = 'https://m.ieduchina.com/api.php?'

	url_pattern = re.compile(r'^\/\/(.*)(m\.ieduchina\.com)(.*)')
	article_id_parttern = re.compile(r'^\/\/.*\/([0-9]+).html$')

	urls = []
	article_ids = []

	def __init__(self, mode = '0', *args, **kwargs):
		super(ArticlesSpider, self).__init__(*args, **kwargs)
		self.mode = int(mode)

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
			# print('[*] visiting user_id: ' +  str(user_id) + ' page : ' + str(page))

			item_links = response.css('div.collect-item h3.title a::attr(href)').extract()
			for a in item_links:
				if self.mode > 0 :
					m = self.url_pattern.search(a)
					if m :
						url_prefix = m.group(1)
						url_base = m.group(3)

						pc_link = url_prefix + 'ieduchina.com' + url_base
						m_link = url_prefix + 'm.ieduchina.com' + url_base

						print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '] pc: ' + pc_link)
						print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']  m: ' + m_link)
						
						self.urls.append(pc_link)
						self.urls.append(m_link)
				else :
					id_m = self.article_id_parttern.search(a)
					if id_m :
						article_id = id_m.group(1)
						counter_params = 'op=count&id=' + article_id + '&modelid=1'
						pc_request_url = self.pc_counter_url + counter_params
						m_request_url = self.m_counter_url + counter_params

						# print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + '] pc: ' + pc_request_url)
						# print('    [' + datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S') + ']  m: ' + m_request_url)
						
						self.urls.append(pc_request_url)
						self.urls.append(m_request_url)
						self.article_ids.append(article_id)

			formdata = {
				'page': str(page + 1),
				'userid': str(user_id)
			}
			yield scrapy.FormRequest(url=self.request_url, method='POST', formdata=formdata, callback=self.parse, meta={'user_id': user_id, 'page' : page + 1})
		else:
			return

	def closed( self, reason ):
		generate_postman_collection(self.article_ids)


	def build_postman_item(self, article_id, pc_mode) :
		counter_params = 'op=count&id=' + article_id + '&modelid=1'
		if(pc_mode) :
			request_url = self.pc_counter_url + counter_params
		else:
			request_url = self.m_counter_url + counter_params
		item = {
			"name": article_id,
			"request": {
				"method": "GET",
				"header": [],
				"body": {
					"mode": "raw",
					"raw": ""
				},
				"url": {
					"raw": request_url,
					"protocol": "https",
					"host": [
						"www",
						"ieduchina",
						"com"
					],
					"path": [
						"api.php"
					],
					"query": [
						{
							"key": "op",
							"value": "count"
						},
						{
							"key": "id",
							"value": article_id
						},
						{
							"key": "modelid",
							"value": "1"
						}
					]
				}
			},
			"response": []
		}

		return item

	def generate_postman_collection(self, article_ids) :
		items = []
		for article_id in article_ids :
			items.append(build_postman_item(article_id, True));
			items.append(build_postman_item(article_id, False));

		data = {
			"info" : {
				"_postman_id": "d38cfd79-91d5-42d9-a8e4-95a33bd1ec4b",
				"name": "ieduchina_collection",
				"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
			},
			"item" : items
		}

		with open('ieduchina_collection.json', 'w') as outfile:
			json.dump(data, outfile)
	