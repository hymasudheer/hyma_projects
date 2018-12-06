import scrapy
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request

class LabnolSpider(scrapy.Spider):
	name = "labnol"
	start_urls = ['https://www.labnol.org/']
	def parse(self, response):
		sel = Selector(response)
		#titles = sel.xpath('//h2[@class="home__title"]/text()').extract()
		#print (titles)
		
		for t in response.css('div.feature_body'):
		
			titles = t.css('h2.home__title::text').extract_first()
		
		#next_page = sel.xpath('//a/@href').extract_first()
		next_page = sel.xpath('//a[@class="btn btn--primary xtype--uppercase"]/@href').extract()
		if next_page is not None:
			next_page = response.urljoin(next_page)
			#yield 
			scrapy.Request(next_page, callback = self.parse)
		#print (titles)
		    
		
		#next_page_url = response.css("a.'btn btn--primary xtype--uppercase'::attr(href)").extract_first()
		#if next_page_url is not None:
		#	yield scrapy.Request(response.urljoin(next_page_url))