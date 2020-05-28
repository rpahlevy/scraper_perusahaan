import re
import urllib


def fix_title(title):
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

def get_slug(title, replace_space=''):
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
    slug = re.sub('[\(\)\/\/]', '', slug)
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

def download(url, to):
    urllib.request.urlretrieve(url, to)