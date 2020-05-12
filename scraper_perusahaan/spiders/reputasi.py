# -*- coding: utf-8 -*-
import scrapy


class ReputasiSpider(scrapy.Spider):
    name = 'reputasi'
    allowed_domains = ['reputasi.co.id']
    start_urls = ['https://reputasi.co.id/categories/']

    def parse(self, response):
        for li in response.css('.all_categories li'):
            category = li.css('a::text').get()
            href = li.css('a::attr(href)').get()
            yield response.follow(href, callback=self.parse_category, meta={'category': category})

    def parse_category(self, response):
        for a in response.css('.custom_review h3 > a'):
            name = a.css('::text').get()
            url = a.css('a::attr(href)').get()
            yield {
                'name': name,
                'url': url,
            }
