# -*- coding: utf-8 -*-
import scrapy
import helpers

class KlikalamatSpider(scrapy.Spider):
    name = 'klikalamat'
    allowed_domains = ['klikalamat.com']
    start_urls = ['http://klikalamat.com/daftar-alamat-terbaru/']

    def parse(self, response):
        for node in response.css('.search_result_listing > .post'):
            node_url = node.css('a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)
        next = response.css('a.next')
        if next is not None:
            yield response.follow(next, callback=self.parse)

    def parse_detail(self, response):
        category = response.css('.breadcrumb-trail > a::text')[1].get()
        name = response.css('h1 span.single-title::text').get() or ''
        address = ''
        city = ''
        phone = ''
        email = ''
        website = ''
        description = []
        url = response.url or ''

        # description
        for txt in response.css('.listing_description h5::text'):
            description.append(txt.get().strip())
        description = '. '.join(description)
        description = description.replace('..', '.')

        # table information
        for tr in response.css('.entry-header-custom-left > p'):
            k = tr.css('label::text').get()
            v = tr.css('span::text').get()
            if len(k) == 0:
                continue
            elif 'Alamat' in k:
                address = v
            elif 'Email' in k:
                email = v
            elif 'Website' in k:
                website = v
            elif 'Telepon' in k:
                phone = v

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
