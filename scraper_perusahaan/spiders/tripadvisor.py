# -*- coding: utf-8 -*-
import scrapy


class TripadvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com']
    start_urls = [
        # 'https://www.tripadvisor.com/Hotels-g294225-Indonesia-Hotels.html',
        'https://www.tripadvisor.com/Restaurants-g294225-Indonesia.html'
    ]

    def parse(self, response):
        url = response.url
        if 'Hotel' in url:
            return self.parse_hotel(response)
        if 'Restaurant' in url:
            return self.parse_restaurant(response)
    def parse_hotel(self, response):
        for node in response.css('a.property_title'):
            node_url = node.css('::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)
        # another category
        for node in response.css('.geo_wrap > a'):
            node_url = node.css('::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_hotel)
        for node in response.css('.geoList > li > a'):
            node_url = node.css('::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_hotel)
        # next category
        next = response.css('.nav.next::attr(href)').get()
        if next is not None:
            yield response.follow(next, callback=self.parse_hotel)
    def parse_restaurant(self, response):
        for node in response.css('a._15_ydu6b'):
            node_url = node.css('::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)
        # another category
        for node in response.css('.geo_name > a'):
            node_url = node.css('::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_restaurant)
        # next category
        next = response.css('.nav.next::attr(href)').get()
        if next is not None:
            yield response.follow(next, callback=self.parse_restaurant)

    def get_category(self, url):
        if 'Hotel' in url:
            return 'Hotel'
        if 'Restaurant' in url:
            return 'Restaurant'
        if 'Vacation' in url:
            return 'Vacation'
        return ''

    def get_email(self, html):
        start_key = 'emergencyEmail\\":'
        end_key = ',\\"emergencyPhone'
        start = html.find(start_key) + len(start_key)
        end = html.find(end_key)
        if start < 0 or end < 0:
            return ''
        text = html[start:end].replace('\\', '').replace('"', '')
        return text or ''

    def get_phone(self, html):
        start_key = 'emergencyPhone\\":'
        end_key = ',\\"userRole'
        start = html.find(start_key) + len(start_key)
        end = html.find(end_key)
        if start < 0 or end < 0:
            return ''
        text = html[start:end].replace('\\', '').replace('"', '')
        return text or ''

    def parse_detail(self, response):
        category = self.get_category(response.url)
        name = response.css('h1#HEADING::text').get() or ''
        address = response.css('._3ErVArsu::text').get() or ''
        city = ''
        phone = self.get_phone(response.text)
        email = self.get_email(response.text)
        website = ''
        description = ''
        url = response.url or ''

        if len(email) == 0:
            self.logger.info('{} : EMPTY EMAIL'.format(url))
        if len(phone) == 0:
            self.logger.info('{} : EMPTY PHONE'.format(url))

        if len(email) > 0 and len(phone) > 0:
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
