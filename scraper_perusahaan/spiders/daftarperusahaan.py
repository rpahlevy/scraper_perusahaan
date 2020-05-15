# -*- coding: utf-8 -*-
import scrapy
import urllib.request

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
        # get url in nav
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
        name = response.css('h2::text').get() or ''
        address = response.css('.node p::text').get() or ''
        city = response.css('.meta .tags a::text').get() or ''
        phone = response.css('.field-field-telepon .field-item::text').get() or ''
        email = response.css('.field-field-email .field-item::text').get() or ''
        website = response.css('.field-field-website .field-item::text').get() or ''
        description = ''
        url = response.url or ''

        if len(email) == 0:
            self.logger.info('{} : EMPTY EMAIL'.format(url))
        if len(phone) == 0:
            self.logger.info('{} : EMPTY PHONE'.format(url))

        if len(email) > 0 and len(phone) > 0:
            image_url = response.css('img::attr(src)').get()
            if image_url is not None:
                image_url = image_url.strip()
                ext = image_url.split('.')[-1]
                image_name = self.get_slug(self.fix_title(name))
                target_dir = 'images/{}/'.format(self.name)
                self.logger.info('downloading image: {} => {}{}'.format(image_url, target_dir, image_name))
                urllib.request.urlretrieve(image_url, target_dir + image_name)
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

    def fix_title(self, title):
        # remove non utf
        title = bytes(title, 'utf-8').decode('utf-8', 'ignore')
        # remove non alpha and some characters
        title = re.sub('[^a-zA-Z0-9 \-,\.]', '', title)
        title = title.strip()
        title = title.strip(' ,.')
        slug = title.lower()
        # helper
        last2 = slug[-2:]
        # remove pt
        if last2 == 'pt':
            title = 'PT ' + title[:-2]
        # remove cv
        if last2 == 'cv':
            title = 'CV ' + title[:-2]
        # strip
        title = title.strip(' ,.')
        return title

    def get_slug(self, title, replace_space=''):
        slug = title.lower().strip()
        slug = slug.strip(' ,.')
        # split by '-'
        if '-' in slug:
            slug = slug.split('-')
            if len(slug[-1].split(' ')) > 3:
                slug[-1] = slug[-1].strip()
                slug = ''.join(slug)
            else:
                slug = ''.join(slug[:-1])
            slug = slug.strip(' ,.')
        # split by '|'
        if '|' in slug:
            slug = slug.split('|')[0]
            slug = slug.strip(' ,.')
        # split by ':'
        if ':' in slug:
            slug = slug.split(':')[0]
            slug = slug.strip(' ,.')
        # remove ()
        slug = re.sub('[\(\)]', '', slug)
        slug = slug.strip(' ,.')
        # skip helper if len <= 4
        if len(slug) <= 4:
            if len(replace_space) > 0:
                slug = re.sub(' ', replace_space, slug).strip()
            return slug
        # helper
        first2 = slug[:2]
        first3 = slug[:3]
        last2 = slug[-2:]
        last3 = slug[-3:]
        last4 = slug[-4:]
        # cek pt & pt.
        if first2 == 'pt':
            slug = slug[2:]
        if last2 == 'pt':
            slug = slug[:-2]
        slug = slug.strip(' ,.')
        # cek cv & cv.
        if first2 == 'cv':
            slug = slug[2:]
        if last2 == 'cv':
            slug = slug[:-2]
        slug = slug.strip(' ,.')
        # cek tbk & tbk.
        if last3 == 'tbk':
            slug = slug[:-3]
        slug = slug.strip(' ,.')
        # cek ltd & ltd.
        if last3 == 'ltd':
            slug = slug[:-3]
        slug = slug.strip(' ,.')
        # cek co & co.
        if last2 == 'co':
            slug = slug[:-2]
        slug = slug.strip(' ,.')
        # replace_space
        if len(replace_space) > 0:
            slug = re.sub(' ', replace_space, slug).strip()
        return slug
