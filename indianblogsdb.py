import datetime
import os
import csv
import mysql.connector

from scrapy import signals
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider
from scrapy.xlib.pydispatch import dispatcher
#from db import *

import sys
reload(sys)
sys.setdefaultencoding("utf-8") 

class Indianblogs(BaseSpider):
	"""Starts name of the Crawler here"""
	name = "indianblogsdb"
	start_urls = ['https://www.topindianblogs.com/']
	
	def __init__(self, *args, **kwargs):
		"""Connecting to Database"""
		self.conn = mysql.connector.connect(host="localhost", user="root", password="hyma22$", db="indianblogsdb", charset='utf8mb4')
		self.cur = self.conn.cursor()
		self.crawl_type = kwargs.get('c_type', 'keepup')
		#self.conn , self.cur = get_pymysql_connection()
		dispatcher.connect(self.spider_closed, signals.spider_closed)
	
	def spider_closed(self, spider):
		query = 'insert into topindianblogs(blog_id) values(%s)'
		#import pdb;pdb.set_trace()
		values = (self.crawl_type, '1')
		self.cur.execute(query, values)
		
	def parse(self, response):
		"""Nodes starts here"""
		sel = Selector(response)
		node = sel.xpath('//div[@class="row row-eq-height"]')
		for data in node:
			category = '-'.join(data.xpath('.//h4/text()').extract()).strip()
			div = data.xpath('.//li[@class="media"]')
			for content in div:
				url = ''.join(content.xpath('.//h5/a/@href').extract()).strip()
				author = (''.join(content.xpath('.//div[@class="media-body"]/text()').extract()).strip()).replace('\r\n', '')
				qry = 'insert into topindianblogs(url, author, category) values(%s, %s, %s)'
				#import pdb;pdb.set_trace();
				values = (url, author, category)
				self.cur.execute(qry, values)
				self.conn.commit()
				