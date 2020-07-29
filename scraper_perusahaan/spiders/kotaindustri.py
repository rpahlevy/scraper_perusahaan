# -*- coding: utf-8 -*-
import scrapy


class KotaindustriSpider(scrapy.Spider):
    name = 'kotaindustri'
    allowed_domains = ['www.kotaindustri.co.id']
    start_urls = ['https://www.kotaindustri.co.id/all-categories/']

    def parse(self, response):
        for node in response.css('#directorist a'):
            node_url = node.css('a::attr(href)').get().strip()
            yield response.follow(node_url, callback=self.parse_category)

    def parse_category(self, response):
        for node in response.css('.atbdp_column .atbd_listing_title > a'):
            node_url = node.css('a::attr(href)').get().strip()
            yield response.follow(node_url, callback=self.parse_detail)

    def parse_detail(self, response):
        contact = response.css('.atbd_contact_information_module')
        if contact is None:
            return
        category = response.css('.directory_tag span a::text').get() or ''
        name = response.css('h1::text').get() or ''
        address = ''
        city = ''
        phone = ''
        email = ''
        website = ''
        description = []
        url = response.url or ''

        # description
        for txt in response.css('.about_detail p::text'):
            description.append(txt.get().strip())
        description = '. '.join(description)
        description = description.replace('..', '.')
        description = description.replace('. . ', '. ')

        # table information
        for tr in response.css('.atbd_contact_info > ul > li'):
            k = tr.css('.atbd_info_title::text').get()
            v = tr.css('.atbd_info::text').get()
            if k is None or len(k) == 0:
                continue
            elif 'Alamat' in k:
                address = v
            elif 'Telepon' in k:
                phone = tr.css('.atbd_info a::text').get()
            elif 'Email' in k:
                email = tr.css('.atbd_info a::text').get()
            elif 'Website' in k:
                website = v

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
