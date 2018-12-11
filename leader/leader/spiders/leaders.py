import datetime
import os
import csv

from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider


class WorldLeaders(BaseSpider):
	name = 'leader'
	start_urls = ['https://www.cia.gov/library/publications/world-leaders-1/']
	
	def __init__(self):
		self.filename = "ciadata%s.csv" % (str(datetime.datetime.now().date()))
		self.csv_file = self.is_path_file_name(self.filename)
		self.fields = ["url", "country", "position", "leader"]
		self.csv_file.writerow(self.fields)
		import pdb;pdb.set_trace()
		
	def is_path_file_name(self, excel_file_name):
		if os.path.isfile(excel_file_name):
			os.system('rm%s' % excel_file_name)
		oupf = open(excel_file_name, 'ab+')
		todays_excel_file = csv.writer(oupf)
		return todays_excel_file
	
	def parse(self, response):
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
		country_name = ''.join(sel.xpath('//div[@id="countryOutput"]//td[@class="countryName"]//span/text()').extract()).strip()
		content = sel.xpath('//div[@style="page-break-inside: !important;"]')
		for data in content:
			leader_position = ''.join(data.xpath('.//span[@class="title"]/span/text()').extract()).strip()
			leader_name = ''.join(data.xpath('//span[@class="cos_name"]/span/text()').extract()).strip()
			csv_values = [reference, country_name, leader_name, leader_position]
			self.csv_file.writerow(csv_values)
	