import scrapy

from scrapy.loader import ItemLoader
from ..items import RaiffeisenluItem
from itemloaders.processors import TakeFirst


class RaiffeisenluSpider(scrapy.Spider):
	name = 'raiffeisenlu'
	start_urls = ['https://www.raiffeisen.lu/fr/banque-raiffeisen/nouvelles-conditions-generales-regissant-les-relations-de-la-banque-raiffeisen']

	def parse(self, response):
		post_links = response.xpath('//a[@class="overlay-link"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//li[@class="pager-next"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)


	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@data-field-name="body"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="date-display-single"]/text()').get()

		item = ItemLoader(item=RaiffeisenluItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
