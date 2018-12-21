import datetime
import os
import csv
import mysql.connector

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

class leaders(BaseSpider):
	"""Starts the name of the crawler"""
	name = 'leaderdb'
	start_urls = ['https://www.cia.gov/library/publications/world-leaders-1/']
	count = 0
	
	def __init__(self, *args, **kwargs):
		""" Connecting to database"""
		self.conn = mysql.connector.connect(host="localhost", user="root", password='hyma22$', db="ciagov", charset='utf8mb4')
		self.cur = self.conn.cursor()
		self.crawl_type = kwargs.get('c_type', 'keepup')
		dispatcher.connect(self.spider_closed, signals.spider_closed)
		
	def spider_closed(self, spider):
		query = 'insert into worldleaders(type, lid) vlaues(%d, %d)'
		values = (self.crawl_type, '1')
		self.cur.execute(query, values)
	
	def parse(self, response):
		"""Nodes start here"""
		sel = Selector(response)
		name = '/'.join(sel.xpath('//div[@id="cosAlphaList"]//ul[@id="cosCountryList"]/li/a/text()').extract()).strip()
		urls = sel.xpath('//div[@id="cosAlphaList"]//@href').extract()
		for url in urls:
			full_link = "https://www.cia.gov/library/publications/resources/world-leaders-1/" + url
			print (full_link)
			yield Request(full_link, callback=self.parse_text)
			
	def parse_text(self, response):
		sel = Selector(response)
		reference = response.url
		country_name = ''.join(sel.xpath('//div[@id="countryOutput"]//td[@class="countryName"]//span//text()').extract()).strip()
		content = sel.xpath('//div[@style="page-break-inside: !important;"]')
		#import pdb;pdb.set_trace();
		for data in content:
			leader_position = ''.join(data.xpath('.//span[@class="title"]//text()').extract()).strip()
			leader_name = ''.join(data.xpath('.//span[@class="cos_name"]//text()').extract()).strip()
			qry = 'insert into worldleaders(country_name, leader_position, leader_name) values(%s, %s, %s)'
			values = (country_name, leader_position, leader_name)
			self.cur.execute(qry, values)
			self.conn.commit()