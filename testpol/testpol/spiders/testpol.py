#pylint: disable=mixed-indentation, line-too-long
import datetime
import os
import csv
from scrapy.http import FormRequest, Request
from scrapy.selector import Selector
from scrapy.spiders import BaseSpider

class Testpol(BaseSpider):
    ''' class starts '''
    name = 'testpol'
    start_domain = ['https://www.interpol.int']
    start_urls = ['https://www.interpol.int/notice/search/wanted']

    def __init__(self, keyword = '', *args, **kwargs):
	    super(Testpol, self).__init__(*args, **kwargs)
	    self.keyword = keyword
	    self.filename = "testpol%s.csv" % (str(datetime.datetime.now().date()))
	    self.csv_file = self.is_path_file_name(self.filename)
	    self.fields = ["url", "Family_name", "Criminal_Name", "sex", "Date_of_birth", "Place_of_birth", "Language_spoken", "Nationality", "Charges", "Regions_where_wanted"]
	    self.csv_file.writerow(self.fields)
		
    def is_path_file_name(self, excel_file_name):
        ''' This function contains csv_file generation '''
        if os.path.isfile(excel_file_name):
		    os.system('rm%s' % excel_file_name)
        oupf = open(excel_file_name, 'ab+')
        todays_excel_file = csv.writer(oupf)
        return todays_excel_file	
	
    def parse(self, response):
        ''' This function contains last pages_ navigations'''
        headers = {
	      'Connection': 'keep-alive',
		  'Cache-Control': 'max-age=0',
          'Origin': 'https://www.interpol.int',
	      'Upgrade-Insecure-Requests': '1',
	      'Content-Type': 'application/x-www-form-urlencoded',
	      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
	      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	      'Referer': 'https://www.interpol.int/notice/search/wanted',
	      'Accept-Encoding': 'gzip, deflate, br',
	      'Accept-Language': 'en-US,en;q=0.9',
		}
        data = [('search', '1'), ('Name', self.keyword), ('Forename', ''), ('Nationality', ''), ('FreeText', ''), ('current_age_mini', '0'), ('current_age_maxi', '100'), ('Sex', ''), ('Eyes', ''), ('Hair', ''), ('RequestingCountry', ''), ('data', ''),]
        yield FormRequest('https://www.interpol.int/notice/search/wanted', callback=self.parse_next, headers=headers, formdata=data)

    def parse_next(self, response):
	    '''
        This function contains required xpaths
        '''
	    sel = Selector(response)
	    urls = sel.xpath('//a[contains(@href, "/notice/search")]/@href').extract()
	    for url in urls:
		    full_url = "https://www.interpol.int" + url
		    yield Request(full_url, self.parse_final_data)
			
    def parse_final_data(self, response):
	    '''
        This function contains required xpaths
        '''
	    sel = Selector(response)
	    reference = response.url
	    family_name = ''.join(sel.xpath('//tr//td[contains(text(), "Present family name:")]/following-sibling::td/text()').extract()).strip()
	    fore_name = ''.join(sel.xpath('//tr//td[contains(text(), "Forename:")]/following-sibling::td/text()').extract()).strip()
	    sex = ''.join(sel.xpath('//tr//td[contains(text(), "Sex:")]/following-sibling::td/text()').extract()).strip()
	    date_of_birth = ''.join(sel.xpath('//tr//td[contains(text(), "Date of birth:")]/following-sibling::td/text()').extract())
	    place_of_birth = ''.join(sel.xpath('//tr//td[contains(text(), "Place of birth:")]/following-sibling::td/text()').extract()).strip()
	    language_spoken = ''.join(sel.xpath('//tr//td[contains(text(), "Language spoken:")]/following-sibling::td/text()').extract()).strip()
	    nationality = ''.join(sel.xpath('//tr//td[contains(text(), "Nationality:")]/following-sibling::td/text()').extract()).strip()
	    charges = ''.join(sel.xpath('//p[@class="charge"]/text()').extract())
	    regions_wanted = ''.join(sel.xpath('//div//span[@class="nom_fugitif_wanted_small"]/text()').extract()).strip()
	    csv_values = [reference, family_name.encode('utf8'), fore_name.encode('utf8'), sex, date_of_birth, place_of_birth, language_spoken, nationality, charges.encode('utf8'), regions_wanted.encode('utf8'),]
	    self.csv_file.writerow(csv_values)