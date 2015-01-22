import re
import scrapy
from flipkart.items import FlipkartItem
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor as LinkExtractor



FLIPKART_BASE_URL = 'http://flipkart.com/'


class FlipkartSpider(CrawlSpider):
    name = 'flipkart'
    allowed_domains = ['flipkart.com']
    
    start_urls = [FLIPKART_BASE_URL + 'computers/laptops?sid=6bo,b5g&otracker=hp_nmenu_sub_electronics_0_Laptops']

    # Extraction rule. Extract the links that have only /laptops/ in the link.
    rules = [Rule(LinkExtractor(allow=['\/laptops\/']), 'parse_laptops')]
    
    def parse_laptops(self, response):
        flipkart_items = list()

        # Here we are getting the items that have offer
        for sel in response.xpath("//div[text()[contains(.,'Offer')]]/ancestor::div[contains(@class,'product-unit')]"):
            
            # For each item getting the info, price and rating.
            info_values = sel.xpath(".//a[contains(@class,'fk-display-block')]/text()").extract()
            price_values = sel.xpath(".//div[contains(@class,'pu-final')]/span/text()").extract()
            rating_values = sel.xpath(".//div[contains(@class, 'pu-rating')]/text()").extract()
            
            
            info = info_values[-1]
            price = price_values[0]
            rating = rating_values[0]

            flipkart_item = FlipkartItem()
            flipkart_item['info'] = info
            flipkart_item['price'] = price
            flipkart_item['rating'] = rating
            
            flipkart_items.append(flipkart_item)
        
        return flipkart_items

    