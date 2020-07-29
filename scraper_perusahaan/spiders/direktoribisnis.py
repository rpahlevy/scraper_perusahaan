# -*- coding: utf-8 -*-
import scrapy


class DirektoribisnisSpider(scrapy.Spider):
    name = 'direktoribisnis'
    allowed_domains = ['direktoribisnis.id']
    start_urls = ['https://direktoribisnis.id/']

    def parse(self, response):
        for node in response.css('.info > h5'):
            node_url = node.css('a::attr(href)').get().strip()
            yield response.follow(node_url, callback=self.parse_category)

    def parse_category(self, response):
        for node in response.css('h3.view-h3 > a'):
            node_url = node.css('::attr(href)').get().strip()
            yield response.follow(node_url, callback=self.parse_detail)
        try:
            next = response.css('ul.pagination > li > a')[-1]
            next_txt = next.css('::text').get()
            if '>' in next_txt:
                next_url = next.css('::attr(href)').get().strip()
                yield response.follow(next_url, callback=self.parse_category)
        except:
            self.logger.info('No next after url: {}'.format(response.url))

    def parse_detail(self, response):
        category = response.css('ol.breadcrumb.pull-left > li > a')[-1].css('::text').get() or ''
        name = response.css('h1.business-title span::text').get() or ''
        address = []
        city = response.css('span[itemprop=addressLocality]::text').get() or ''
        phone = response.css('span[itemprop=telephone]::text').get() or ''
        email = ''
        website = response.css('ul.dropdown-menu > li > a[itemprop=url]::attr(href)').get() or ''
        description = []
        url = response.url or ''

        # email
        try:
            cfemail = response.css('span.__cf_email__::attr(data-cfemail)').get() or ''
            if len(cfemail) > 0:
                email = helpers.cfDecodeEmail(cfemail)
        except:
            email = ''

        # address
        address_1 = response.css('h4 > span > span::text')
        address_2 = response.css('h4 > span::text')
        for index, a1 in enumerate(address_1):
            a1 = a1.get().strip()
            a2 = address_2[index].get().strip()
            address.append(a1)
            address.append(a2)
        address = ' '.join(address)
        address = address.replace(' ,', ',')

        # description
        for txt in response.css('.col-sm-12 > p'):
            description.append(txt.get().strip())
        description = '. '.join(description)
        description = description.replace('..', '.')
        description = description.replace('. . ', '. ')
        description = description.replace('. . ', '. ')

        if len(email) == 0:
            self.logger.info('{} : EMPTY EMAIL'.format(url))
        if len(phone) == 0:
            self.logger.info('{} : EMPTY PHONE'.format(url))

        if len(email) > 0 and len(phone) > 0:
            image_url = response.css('.detail-listing-img > img::attr(src)').get()
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
