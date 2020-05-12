# -*- coding: utf-8 -*-
import scrapy


class DaftarperusahaanSpider(scrapy.Spider):
    name = 'daftarperusahaan'
    allowed_domains = ['www.daftarperusahaan.com']
    start_urls = ['https://www.daftarperusahaan.com/']

    def parse(self, response):
        # get url in nav
        for href in response.css('#navigasi > a::attr(href)'):
            if 'bidang' not in href.get():
                continue
            yield response.follow(href, callback=self.parse_category)
        # get url in nav
        for href in response.css('.frontarea > li > a::attr(href)'):
            if 'bidang' not in href.get():
                continue
            yield response.follow(href, callback=self.parse_category)

    def parse_category(self, response):
        # get list perusahaan
        for node in response.css('.node'):
            node_url = node.css('a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)

        # get next page url
        next_url = response.css('.pager-next > a::attr(href)').get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse_category)

    def parse_detail(self, response):
        category = response.css('.meta .category a::text').get().strip()
        name = response.css('h2::text').get().strip()
        address = response.css('.node p::text').get().strip()
        city = response.css('.meta .tags a::text').get().strip()
        phone = response.css('.field-field-telepon .field-item::text').get().strip()
        email = response.css('.field-field-email .field-item::text').get().strip()
        website = response.css('.field-field-website .field-item::text').get().strip()
        description = response.css('.meta .tags::text')[-1].get().strip()
        url = response.url
        yield {
            'category': category,
            'name': name,
            'address': address,
            'city': city,
            'phone': phone,
            'email': email,
            'website': website,
            'description': description,
            'url': url,
        }
