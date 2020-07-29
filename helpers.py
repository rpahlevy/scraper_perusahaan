import re
import os
import requests


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

def remove_fix(slug):
    slug = slug.strip(' ,.')
    # skip if len <= 4
    if len(slug) <= 4:
        return slug
    # helper
    first2 = slug[:2]
    last2 = slug[-2:]
    last3 = slug[-3:]
    # cek pt & pt.
    if first2 == 'pt':
        slug = slug[2:]
        return remove_fix(slug)
    if last2 == 'pt':
        slug = slug[:-2]
        return remove_fix(slug)
    slug = slug.strip(' ,.')
    # cek cv & cv.
    if first2 == 'cv':
        slug = slug[2:]
        return remove_fix(slug)
    if last2 == 'cv':
        slug = slug[:-2]
        return remove_fix(slug)
    slug = slug.strip(' ,.')
    # cek tbk & tbk.
    if last3 == 'tbk':
        slug = slug[:-3]
        return remove_fix(slug)
    slug = slug.strip(' ,.')
    # cek ltd & ltd.
    if last3 == 'ltd':
        slug = slug[:-3]
        return remove_fix(slug)
    slug = slug.strip(' ,.')
    # cek co & co.
    if last2 == 'co':
        slug = slug[:-2]
        return remove_fix(slug)
    slug = slug.strip(' ,.')
    return slug

def get_slug(title, replace_space='', remove_city=False):
    slug = title.lower().strip()
    slug = slug.strip(' ,.')
    # remove ()
    slug = re.sub('[\(\)\/\\\]', '', slug)
    slug = slug.strip(' ,.')
    # skip helper if len <= 4
    if len(slug) <= 4:
        if len(replace_space) > 0:
            slug = re.sub(' ', replace_space, slug).strip(' ,.')
        return slug
    # remove prepend / append
    slug = remove_fix(slug)
    # remove city?
    if remove_city:
        # split by ' - '
        if ' - ' in slug:
            slug = slug.split(' - ')
            slug = ' '.join(slug[:-1])
            slug = slug.strip(' ,.')
    # split by '-'
    if '-' in slug:
        slug = slug.split('-')
        # if len(slug[0]) <= 5 or len(slug[-1]) <= 5 or len(slug[-1].split(' ')) > 3:
        #     slug[-1] = slug[-1].strip()
        #     slug = ''.join(slug)
        # else:
        #     slug = ''.join(slug[:-1])
        slug = ' '.join(slug)
        slug = slug.strip(' ,.')
    # split by '|'
    if '|' in slug:
        slug = slug.split('|')[0]
        slug = slug.strip(' ,.')
    # split by ':'
    if ':' in slug:
        slug = slug.split(':')[0]
        slug = slug.strip(' ,.')
    # remove prepend / append
    slug = remove_fix(slug)
    # remove extra space
    slug = re.sub('  ', ' ', slug)
    slug = re.sub('  ', ' ', slug)
    slug = re.sub('  ', ' ', slug)
    # replace_space
    if len(replace_space) > 0:
        slug = re.sub(' ', replace_space, slug).strip()
    slug = slug.strip(' ,.')
    return slug

def download(url, to):
    # cek if file exists
    if os.path.exists(to) and os.path.getsize(to) > 0:
        return True
    r = requests.get(url)
    if r.status_code == 200:
        with open(to, 'wb') as f:
            f.write(r.content)
        return True
    else:
        return False

def cfDecodeEmail(encodedString):
    r = int(encodedString[:2],16)
    email = ''.join([chr(int(encodedString[i:i+2], 16) ^ r) for i in range(2, len(encodedString), 2)])
    return email