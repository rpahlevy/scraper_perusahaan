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
            yield response.follow(next_page, self.parse)

    def parse_category(self, response):
        for href in response.css('h3.panel-title a::attr(href)'):
            yield response.follow(href, self.parse_detail)

        # get next page
        select_next = False
        next_page = None
        for li in response.css('.pagination '):
            if select_next:
                next_page = li.css('a::attr(href)')
                break
            if 'disabled' in li.css('::attr(class)').get():
                select_next = True
        if next_page is not None:
            yield response.follow(next_page)

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
            panel_body = panel.css('.panel-body::text').get().strip()
            if 'Alamat' in panel_title:
                address = panel_body
            elif 'Telepon' in panel_title:
                phone = panel_body
            elif 'Website' in panel_title:
                website = panel_body
            elif 'Email' in panel_title:
                email = panel_body
            elif 'Tentang' in panel_title:
                description = panel_body

        if len(email) == 0 or len(phone) == 0:
            return

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
