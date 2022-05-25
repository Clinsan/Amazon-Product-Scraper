from numpy import product
import scrapy
from ..items import AmazonBotItem
import csv
import pandas as pd
product_list=[]
product_name_list=[]
product_price_list=[]
review_list=[]
ratings_list=[]
product_d_list=[]
asin_list=[]
manufacturer=[]
class AmazonSpider(scrapy.Spider):
    name = 'amazon'
    page_number=2
    start_urls = ['https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1']
    #Part-1
    def parse(self, response):
        items=AmazonBotItem()
        product_url = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "s-image-fixed-height", " " ))]/parent::node()/@href').getall()
        product_name = response.css('.a-size-medium.a-text-normal::text').extract()
        product_price = response.css('.a-section .sg-row .a-price-whole ::text ').extract()
        num_reviews = response.css('.s-link-style .s-underline-text::text').extract()
        ratings = response.css('.faceout-product-review .aok-align-bottom , .a-spacing-top-small .aok-align-bottom').css('::text').extract()

        for product in product_url:
            product_list.append("https://www.amazon.in"+product)
        for product_n in product_name:
            product_name_list.append(product_n)
        for product_p in product_price:
            product_price_list.append(product_p)
        for product_r in num_reviews:
            review_list.append(product_r)
        for product_rs in ratings:
            ratings_list.append(product_rs)
            
        items['product_name']=product_name
        items['product_price']=product_price
        items['num_reviews']=num_reviews
        items['rating']=ratings
        items['product_url']=product_url

        yield items

        
            
        next_page = 'https://www.amazon.in/s?k=bags&page='+str(AmazonSpider.page_number)+'&crid=2M096C61O4MLT&qid=1653417177&sprefix=ba%2Caps%2C283&ref=sr_pg_2'
        if AmazonSpider.page_number <= 25:
            AmazonSpider.page_number+=1
            yield response.follow(next_page,callback=self.parse)
        else:
            stp=len(product_list)
            yield scrapy.Request(product_list[0],callback=self.product_parse)

    #Part-2
    def product_parse(self,response):
        items=AmazonBotItem()
        product_description = response.css('#feature-bullets .a-list-item').css('::text').extract()
        product_asin = response.css('li:nth-child(4) .a-text-bold+ span::text ').extract()
        product_manufacturer = response.css('li:nth-child(8) .a-text-bold+ span ::text ').extract()

        for product_d in product_description:
            product_d_list.append(product_d)
        for product_a in product_asin:
            asin_list.append(product_a)
        for product_m in product_manufacturer:
            manufacturer.append(product_m)

        items['product_description']=product_description
        items['product_asin']=product_asin
        items['product_manufacturer']=product_manufacturer

        yield items

        for product in range(1,len(product_list)):
            next_page=product_list[product]
            yield scrapy.Request(next_page,callback=self.product_parse)
        AmazonSpider.exp_csv()

    #Exporting data to csv file
    def exp_csv():
        fields=['Product_URL','Product_name','Product_Price','Num_Reviews','Ratings','Product Description','Product_ASIN','Manufacturer']        
        rows = zip(product_list, product_name_list, product_price_list, review_list, ratings_list,product_d_list,asin_list,manufacturer)
        with open('Scraped_data.csv', "w",encoding="utf-8",newline="") as f:
            writer = csv.writer(f)
            writer.writerow(fields)
            writer.writerows(rows)
        f.close





        