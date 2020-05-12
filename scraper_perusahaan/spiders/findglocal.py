# -*- coding: utf-8 -*-
import scrapy


class FindglocalSpider(scrapy.Spider):
    name = 'findglocal'
    allowed_domains = ['www.findglocal.com']
    start_urls = [
        'http://www.findglocal.com/ID/cities/A',
        'http://www.findglocal.com/ID/cities/B',
        'http://www.findglocal.com/ID/cities/C',
        'http://www.findglocal.com/ID/cities/D',
        'http://www.findglocal.com/ID/cities/E',
        'http://www.findglocal.com/ID/cities/F',
        'http://www.findglocal.com/ID/cities/G',
        'http://www.findglocal.com/ID/cities/H',
        'http://www.findglocal.com/ID/cities/I',
        'http://www.findglocal.com/ID/cities/J',
        'http://www.findglocal.com/ID/cities/K',
        'http://www.findglocal.com/ID/cities/L',
        'http://www.findglocal.com/ID/cities/M',
        'http://www.findglocal.com/ID/cities/N',
        'http://www.findglocal.com/ID/cities/O',
        'http://www.findglocal.com/ID/cities/P',
        'http://www.findglocal.com/ID/cities/Q',
        'http://www.findglocal.com/ID/cities/R',
        'http://www.findglocal.com/ID/cities/S',
        'http://www.findglocal.com/ID/cities/T',
        'http://www.findglocal.com/ID/cities/U',
        'http://www.findglocal.com/ID/cities/V',
        'http://www.findglocal.com/ID/cities/W',
        'http://www.findglocal.com/ID/cities/X',
        'http://www.findglocal.com/ID/cities/Y',
        'http://www.findglocal.com/ID/cities/Z',
    ]

    def parse(self, response):
        for href in response.css('.townlist a::attr(href)'):
            yield response.follow(href, callback=self.parse_city)

    def parse_city(self, response):
        for href in response.css('.col-lg-4.col-md-6.col-xs-12 a::attr(href)'):
            yield response.follow(href, callback=self.parse_category)

    def parse_category(self, response):
        for item in response.css('.inneritembox'):
            href = item.css('a::attr(href)')[0]
            yield response.follow(href, callback=self.parse_detail)

    def parse_detail(self, response):
        category = response.css('.breadcrumb a::text')[3].get() or ''
        name = response.css('h1::text').get() or ''
        address = ' '.join([addr.get().strip() for addr in response.css('.address::text')]) or ''
        city = response.css('.breadcrumb a::text')[2].get() or ''
        phone = response.css('[itemprop=telephone]::text').get() or ''
        email = ''
        website = response.css('.bio.website a::attr(href)').get() or ''
        description = response.css('[itemprop=description]::text').get() or ''
        url = response.url or ''
        yield {
            'category': category.strip(),
            'name': name.strip(),
            'address': address.strip(),
            'city': city.strip(),
            'phone': phone.strip(),
            'email': email.strip(),
            'website': website.strip(),
            'description': description.strip(),
            'url': url.strip(),
        }
