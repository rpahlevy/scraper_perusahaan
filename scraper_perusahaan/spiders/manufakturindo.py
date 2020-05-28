# -*- coding: utf-8 -*-
import scrapy
import helpers


class ManufakturindoSpider(scrapy.Spider):
    name = 'manufakturindo'
    allowed_domains = ['manufakturindo.com']
    start_urls = ['https://manufakturindo.com/company/']

    def parse(self, response):
        # get list perusahaan
        for node in response.css('.list-compy'):
            node_url = node.css('.main-list-compy > .list-content > a::attr(href)').get()
            yield response.follow(node_url, callback=self.parse_detail)
        # get next page url
        next_url = response.css('.pagination-next > a::attr(href)').get()
        if next_url is not None:
            yield response.follow(next_url, callback=self.parse)

    def parse_detail(self, response):
        category = ''
        name = ''
        address = ''
        city = ''
        phone = ''
        fax = ''
        email = ''
        website = ''
        description = ''
        url = response.url or ''
        image_url = ''
        # check type
        lis = response.css('.comp-body li')
        trs = response.css('table.table.description tr')
        if len(lis) > 0:
            # type 1
            for li in lis:
                k = li.css('::text').get().strip().split(':')[0].strip()
                v = li.css('::text').get().strip().split(':')[-1].strip()
                if len(k) == 0:
                    continue
                if 'Company Name' in k:
                    name = v
                elif 'Address' in k:
                    address = v
                elif 'Telephone' in k:
                    phone = li.css('a::text').get().strip()
                elif 'Fax' in k:
                    fax = v
                elif 'Email' in k:
                    email = li.css('a::text').get().strip()
            # description
            description = []
            for p in response.css('.comp-row > p::text'):
                txt = p.get().strip()
                if len(txt) == 0 or 'Description' in txt:
                    continue
                description.append(txt)
            description = ' '.join(description)
            # website
            website = response.css('.comp-row > p > a::attr(href)').get() or ''
            if self.name in website:
                website = ''
            # category
            category = response.css('.title-comp .col-sm-10::text')[-1].get()
            # image_url
            image_url = response.css('.img-container img::attr(src)').get() or ''
        elif len(trs) > 0:
            # type 2
            for tr in trs:
                k = tr.css('td::text')[0].get()
                v = tr.css('td::text')[-1].get()
                if len(k) == 0:
                    continue
                if 'Nama Perusahaan' in k:
                    name = v
                elif 'Alamat' in k:
                    address = tr.css('td')[-1].css('p::text').get()
                elif 'Kategori' in k:
                    category = v
                elif 'Telepon' in k:
                    phone = tr.css('td')[-1].css('a::text').get()
                elif 'Fax' in k:
                    fax = tr.css('td')[-1].css('a::text').get()
                elif 'Email' in k:
                    email = tr.css('td')[-1].css('a::text').get()
            # description
            description = []
            for p in response.css('.container > p::text'):
                txt = p.get().strip()
                if len(txt) == 0:
                    continue
                description.append(txt)
            description = ' '.join(description)
            # website
            website = response.css('a.btn.btn-contactus.btn-go-to::attr(href)').get() or ''
            if self.name in website:
                website = ''
            # image_url
            image_url = response.css('img.center-img::attr(src)').get() or ''

        if len(email) == 0:
            self.logger.info('{} : EMPTY EMAIL'.format(url))
        if len(phone) == 0:
            self.logger.info('{} : EMPTY PHONE'.format(url))

        # if len(email) > 0 and len(phone) > 0:
        name = helpers.fix_title(name)
        slug = helpers.get_slug(name)
        if image_url is not None and len(image_url) > 0:
            image_url = image_url.strip()
            ext = image_url.split('.')[-1]
            image_name = slug
            target_dir = 'images/{}.{}'.format(image_name, ext)
            self.logger.info('downloading image: {} => {}'.format(image_url, target_dir))
            urllib.request.urlretrieve(image_url, target_dir)
        yield {
            'category': category.strip(),
            'name': name.strip(),
            'slug': slug.strip(),
            'address': address.strip(),
            'city': city.strip(),
            'phone': phone.strip(),
            'email': email.strip(),
            'website': website.strip(),
            'description': description.strip(),
            'url': url.strip(),
        }
