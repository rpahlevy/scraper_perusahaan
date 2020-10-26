# -*- coding: utf-8 -*-
import scrapy
import helpers

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
        # get url in paragraph
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
        category = response.css('.meta .category a::text').get() or ''
        name = helpers.fix_title(response.css('h2::text').get() or '')
        slug = helpers.get_slug(name)
        address = response.css('.node p::text').get() or ''
        city = response.css('.meta .tags a::text').get() or ''
        phone = response.css('.field-field-telepon .field-item::text').get() or ''
        fax = response.css('.field-field-fax .field-item::text').get() or ''
        email = response.css('.field-field-email .field-item::text').get() or ''
        website = response.css('.field-field-website .field-item::text').get() or ''
        broker = response.css('.field-field-broker .field-item::text').get() or ''
        npwp = response.css('.field-field-npwp .field-item::text').get().replace('NPWP', '').strip('\n :') or ''
        description = ''
        url = response.url or ''
        image_name = ''

        # if len(email) == 0:
        #     self.logger.info('{} : EMPTY EMAIL'.format(url))
        # if len(phone) == 0:
        #     self.logger.info('{} : EMPTY PHONE'.format(url))

        if self.name in website:
            website = ''

        # if len(email) > 0 and len(phone) > 0:
        image_url = response.css('img::attr(src)').get()
        if image_url is not None:
            image_url = image_url.strip()
            ext = image_url.split('.')[-1]
            image_name = slug
            target_dir = 'images/{}/{}.{}'.format(self.name, image_name, ext)
            self.logger.info('downloading image: {} => {}'.format(image_url, target_dir))
            r = helpers.download(image_url, target_dir)
            if not r:
                self.logger.info('Failed download {} => {}'.format(image_url, target_dir))
        yield {
            'category': category.strip(),
            'name': name.strip(),
            'slug': slug.strip(),
            'address': address.strip(),
            'city': city.strip(),
            'phone': phone.strip(),
            'fax': fax.strip(),
            'email': email.strip(),
            'website': website.strip(),
            'broker': broker.strip(),
            'npwp': npwp.strip(),
            'description': description.strip(),
            'url': url.strip(),
            'image_name': image_name.strip(),
        }
