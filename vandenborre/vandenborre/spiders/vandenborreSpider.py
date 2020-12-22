import logging
import scrapy
import os
from scrapy import Spider

logger = logging.getLogger(__name__)

class VandenBorreSpider(Spider):
    name = "vandenborre.be"
    start_urls = [
        "https://www.vandenborre.be/sitemap/nl/default/",
        # "https://www.vandenborre.be/sitemap/fr/default/",
        ]
    
    def parse(self, response):
        for section in response.css('.border-btm-grey-sm.margin-btm-10-sm'):
            if not section:
                continue
            for goto in section.css('.listicon.clearfix.margin-btm-60-md.margin-btm-20-sm.margin-top-20-sm.js-content.hide-sm .nolist.flex.flex-wrap .col-xs-12.col-md-3 a::attr(href)').extract():
                goto = response.urljoin(goto)
                yield scrapy.Request(url=goto, callback=self.get_each_brand_li)

    def get_each_brand_li(self, response):
        for link in response.css('.border-btm-grey-sm.margin-btm-10-sm'):
            if not link:
                continue
            for goto in link.css('.listicon.clearfix.margin-btm-60-md.js-content.margin-btm-20-sm.margin-top-20-sm.hide-sm .nolist.flex.flex-wrap .col-xs-12.col-md-3 a::attr(href)').extract():
                goto = response.urljoin(goto)
                yield scrapy.Request(url=goto, callback=self.get_product_data)

    def get_product_data(self, response):
        pdf_files = response.css('.js-specs-doc.clearfix .doc-link.flex div>a::attr(href)').extract()
        # if len(pdf_files):
        #     return
        for pdf in pdf_files:
            pdf = pdf.replace(' ', '%20') # removing spaces from the pdf link
            brand = response.css('.product-detail-title.no-margin-btm a *::text').extract_first()
            print(brand, '---------------')
            thumb = response.css('.image-gallery-main-image.js-image-gallery-main-image.js-image-zoom-image.image-gallery-main-image-0::attr(data-large-image)').extract_first()
            thumb = response.urljoin(thumb)
            

        # manual = Manual()
        # product_title = response.css('.product_title.entry-title::text').get().strip()
        # manual['brand'] = self.find_product_brand(product_title)
        # manual['model'] = self.find_product_model(manual['brand'], product_title)
        # manual['product'] = self.find_product_name(manual['brand'], manual['model'],product_title)
        
        # manual['source'] = self.name
        # manual['file_urls'] = [response.urljoin(file)]
        # manual['type'] = self.get_manual_type(response)
        # manual['thumb'] = 'https:'+ response.css('.op_0.attachment-shop_single.size-shop_single.sp-post-image::attr(data-large_image)').extract()[0]
        # manual['url'] = response.urljoin('')  
        # # manual['files'] = []
        # print(manual)
        # yield manual

