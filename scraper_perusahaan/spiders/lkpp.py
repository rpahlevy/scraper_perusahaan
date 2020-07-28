# -*- coding: utf-8 -*-
import scrapy
import helpers

class LkppSpider(scrapy.Spider):
    name = 'lkpp'
    allowed_domains = ['direktori.lkpp.go.id']
    start_urls = ['http://direktori.lkpp.go.id/']

    def parse(self, response):
        for node in response.css('.col-4 > a'):
            node_url = node.css('a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_category)

    def parse_category(self, response):
        for node in response.css('ul.type-list > li > a'):
            node_url = node.css('a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_city)

    def parse_city(self, response):
        for node in response.css('ul.business-list > li > h2 > a'):
            node_url = node.css('a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)

    def parse_detail(self, response):
        category = ''
        name = response.css('h1::text').get() or ''
        address = ''
        city = ''
        phone = ''
        email = ''
        website = ''
        description = []
        url = response.url or ''

        # description
        for txt in response.css('.content > p::text'):
            description.append(txt.get().strip())
        description = '. '.join(description)
        description = description.replace('..', '.')

        # table information
        for tr in response.css('.information table tr'):
            k = tr.css('td::text')[0].get()
            v = tr.css('td::text')[-1].get()
            if len(k) == 0:
                continue
            if 'Nama' in k:
                name = v
            elif 'Kota' in k:
                city = v
            elif 'Alamat' in k:
                address = v
            elif 'Telepon' in k:
                phone = v
            elif 'Email' in k:
                email = v
            elif 'Bidang Usaha' in k:
                category = v
            elif 'Website' in k:
                website = v

        if len(email) == 0:
            self.logger.info('{} : EMPTY EMAIL'.format(url))
        if len(phone) == 0:
            self.logger.info('{} : EMPTY PHONE'.format(url))

        if len(email) > 0 and len(phone) > 0:
            image_url = response.css('img::attr(src)').get()
            if image_url is not None and image_url[-1] != '/':
                image_url = image_url.strip()
                ext = image_url.split('.')[-1]
                image_name = helpers.get_slug(helpers.fix_title(name))
                target_dir = 'images/{}/{}'.format(self.name, image_name)
                self.logger.info('downloading image: {} => {}'.format(image_url, target_dir))
                helpers.download(image_url, target_dir)
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
