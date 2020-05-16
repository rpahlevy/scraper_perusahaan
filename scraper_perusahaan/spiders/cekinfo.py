# -*- coding: utf-8 -*-
import scrapy


class CekinfoSpider(scrapy.Spider):
    name = 'cekinfo'
    allowed_domains = ['www.cekinfo.com']
    start_urls = ['https://www.cekinfo.com/kategori.php']

    def parse(self, response):
        for href in response.css('.result-kategori div strong a::attr(href)'):
            yield response.follow(href, self.parse_category)

        next_page = response.css('.pagination li[style=""] a::attr(href)')
        if next_page is not None:
            yield response.follow(next_page.get(), self.parse)

    def parse_category(self, response):
        for href in response.css('h3.panel-title a::attr(href)'):
            yield response.follow(href, self.parse_detail)

        # get next page
        select_next = False
        next_page = None
        for li in response.css('.pagination li'):
            if select_next:
                next_page = li.css('a::attr(href)')
                break
            li_class = li.css('::attr(class)').get()
            if li_class is not None and 'disabled' in li_class:
                select_next = True
        if next_page is not None:
            yield response.follow(next_page.get(), self.parse_category)

    def parse_detail(self, response):
        category = response.css('.breadcrumb li')[-2].css('::text').get() or ''
        name = response.css('.breadcrumb li')[-1].css('::text').get() or ''
        address = ''
        city = ''
        phone = ''
        email = ''
        website = ''
        description = ''
        url = response.url or ''

        for panel in response.css('.panel'):
            panel_title = panel.css('.col-xs-10.col-sm-11::text').get().strip()
            if 'Alamat' in panel_title:
                address = []
                for addr in panel.css('.panel-body::text'):
                    address.append(addr.get().strip())
                address = ', '.join(address)
            elif 'Telepon' in panel_title:
                phone = panel.css('.panel-body::text').get().strip()
            elif 'Website' in panel_title:
                website = panel.css('.panel-body a::attr(href)').get().strip()
                if self.allowed_domains[0] in website:
                    website = ''
            elif 'Email' in panel_title:
                email = panel.css('.panel-body a::attr(href)').get().replace('mailto:', '')
            elif 'Tentang' in panel_title:
                description = []
                for desc in panel.css('.panel-body::text'):
                    description.append(desc.get().strip())
                description = ' '.join(description).strip()
                if len(description) == 0:
                    for desc in panel.css('.panel-body p::text'):
                        desc = desc.get().strip()
                        if len(desc) >= 200:
                            description = desc
                            break

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
