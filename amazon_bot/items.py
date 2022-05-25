# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonBotItem(scrapy.Item):
    product_url = scrapy.Field()
    product_name = scrapy.Field()
    product_price = scrapy.Field()
    rating = scrapy.Field()
    num_reviews = scrapy.Field()
    product_description = scrapy.Field()
    description = scrapy.Field()
    product_asin = scrapy.Field()
    product_manufacturer = scrapy.Field()
    pass
